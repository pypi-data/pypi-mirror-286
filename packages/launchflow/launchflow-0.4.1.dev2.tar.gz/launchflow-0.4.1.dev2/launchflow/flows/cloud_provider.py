import asyncio
import os
import platform
import subprocess
import tarfile
import time
import webbrowser
import zipfile
from enum import Enum
from typing import Optional

import beaupy
import requests
import rich
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

from launchflow.clients import LaunchFlowAsyncClient
from launchflow.config import config
from launchflow.exceptions import LaunchFlowRequestFailure

XML_TEMPLATE = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <array>
    <dict>
      <key>choiceAttribute</key>
      <string>customLocation</string>
      <key>attributeSetting</key>
      <string>{install_dir}</string>
      <key>choiceIdentifier</key>
      <string>default</string>
    </dict>
  </array>
</plist>
"""


class CloudProvider(Enum):
    GCP = "gcp"
    AWS = "aws"
    AZURE = "azure"


CLOUD_PROVIDER_CHOICES = [
    (CloudProvider.GCP, "Google Cloud Platform"),
    (CloudProvider.AWS, "Amazon Web Services"),
    # (CloudProvider.AZURE, "Microsoft Azure"),
]


def select_cloud_provider() -> CloudProvider:
    options = [f"{f[0].value.upper()} - {f[1]}" for f in CLOUD_PROVIDER_CHOICES]
    answer = beaupy.select(options=options, return_index=True)
    rich.print(f"[pink1]>[/pink1] {options[answer]}")
    return CLOUD_PROVIDER_CHOICES[answer][0]


async def connect(
    client: LaunchFlowAsyncClient,
    account_id: Optional[str],
    provider: Optional[CloudProvider],
):
    account_id = config.get_account_id()
    if provider is None:
        print(
            f"\nSelect the cloud provider you would like to configure for your account ({account_id}):"
        )
        provider = select_cloud_provider()

    setup_status = await client.connect.status(
        account_id=account_id, include_aws_template_url=True
    )
    if provider == CloudProvider.GCP:
        if setup_status.gcp_connection_info.verified_at:
            reverify = beaupy.confirm(
                "[green bold] GCP has already been connected. Would you like to re-verify your connection? [/green bold]",
            )
            if reverify:
                await _connect_gcp(
                    client,
                    account_id,
                    setup_status.gcp_connection_info.admin_service_account_email,
                    add_permissions=False,
                )
            else:
                _setup_local_gcp_env()
        else:
            await _connect_gcp(
                client,
                account_id,
                setup_status.gcp_connection_info.admin_service_account_email,
                add_permissions=True,
            )
    elif provider == CloudProvider.AWS:
        if setup_status.aws_connection_info.verified_at:
            reverify = beaupy.confirm(
                "[green bold] AWS has already been connected. Would you like to re-verify your connection? [/green bold]",
            )
            if reverify:
                await _connect_aws(
                    client,
                    account_id,
                    setup_status.aws_connection_info.external_role_id,
                    setup_status.aws_connection_info.cloud_foundation_template_url,
                )
            else:
                _setup_local_aws_env()
        else:
            await _connect_aws(
                client,
                account_id,
                setup_status.aws_connection_info.external_role_id,
                setup_status.aws_connection_info.cloud_foundation_template_url,
            )
    else:
        raise ValueError(f"LaunchFlow currently does not support `{provider.value}`")


AWS_REGIONS = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
    "af-south-1",
    "ap-east-1",
    "ap-south-2",
    "ap-southest-3",
    "ap-southeast-4",
    "ap-south-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1",
    "ca-central-1",
    "ca-west-1",
    "eu-central-1",
    "eu-central-2",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "eu-south-1",
    "eu-south-2",
    "eu-north-1",
    "il-central-1",
    "me-south-1",
    "me-central-1",
    "sa-east-1",
    "us-gov-east-1",
    "us-gov-west-1",
]

_AWS_URL = "https://{region}.console.aws.amazon.com/cloudformation/home?region={region}#/stacks/create/review?stackName=LaunchFlowRole&param_LaunchFlowExternalID={external_id}&templateURL={template_url}"


def _setup_local_aws_env(ask: bool = True):
    answer = True
    if ask:
        answer = beaupy.confirm(
            "Would you like us to verify your local AWS setup?", default_is_yes=True
        )
    if answer:
        process = subprocess.run("aws --version", shell=True, capture_output=True)
        if process.returncode == 127:
            rich.print("[red]Error: `aws` CLI is not installed on your machine[/red].")
            install = beaupy.confirm(
                "Would you like to install it? (we will follow the steps outlined on https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)",
                default_is_yes=True,
            )
            if not install:
                return
            install_dir = beaupy.prompt(
                "Which directory would you like to install `aws` to (defaults to your home directory `~/aws`)?",
                initial_value="~/aws",
            )
            if install_dir == "~/aws":
                install_dir = os.path.expanduser(install_dir)
            system = platform.system()
            download_url = ""
            proc_type = ""
            is_mac = None
            if system == "Darwin":
                is_mac = True
                proc = subprocess.run("uname -m", shell=True, capture_output=True)
                proc_type = proc.stdout.decode("utf-8").strip()
                if proc.returncode != 0:
                    rich.print(
                        "[red]Error: failed to determine your processor type.[/red]."
                    )
                    return
                if proc_type == "arm64":
                    download_url = "https://awscli.amazonaws.com/AWSCLIV2.pkg"
                elif proc_type == "x86_64":
                    download_url = "https://awscli.amazonaws.com/AWSCLIV2.pkg"
                else:
                    rich.print(
                        f"[red]Error: Processor not supported: {proc_type}.[/red] You can manually install aws following the instructions at: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html, please reach out to us at founders@launchflow.com to have us add support for your machine type."
                    )
                    return
            elif system == "Linux":
                is_mac = False
                proc_type = platform.machine()
                if proc_type == "x86_64":
                    download_url = (
                        "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
                    )
                elif proc_type == "x86":
                    download_url = (
                        "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
                    )
                elif proc_type == "arm64":
                    download_url = (
                        "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip"
                    )
                else:
                    rich.print(
                        f"[red]Error: Processor not supported: {proc_type}[/red]. You can manually install aws following the instructions at: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html, please reach out to us at founders@launchflow.com to have us add support for your machine type."
                    )
                    return
            else:
                # TODO: support windows
                rich.print(
                    f"[red]Error: OS not supported: {system}. You can manually install gcloud following the instructions at: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html[/red]"
                )
                return
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
            ) as progress:
                download_task = progress.add_task(
                    f"Downloading aws for {system} {proc_type}..."
                )
                response = requests.get(download_url, stream=True)
                if response.status_code != 200:
                    rich.print(
                        f"[red]Error: failed to download aws from: {download_url}.[/red]."
                    )
                    return

                file_name = "aws.zip"
                if is_mac:
                    file_name = "AWSCLIV2.pkg"
                file_path = os.path.join(install_dir, file_name)
                os.makedirs(install_dir, exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(response.raw.read())
                progress.remove_task(download_task)
                progress.console.print(
                    f"[green]✓[/green] Downloaded aws for {system} {proc_type}."
                )

            if is_mac:
                is_apple_silicon = proc_type == "arm64"
                if is_apple_silicon:
                    # Check if rosetta is installed
                    rosetta_check = subprocess.run("pgrep -q oahd", shell=True)
                    if rosetta_check.returncode != 0:
                        rich.print(
                            "[red]Error: Rosetta is not installed.[/red] This requires sudo permissions, so we cannot run it on your behalf.\n"
                        )
                        # Prompts the user to run the command and then continues on with the installation when they hit enter
                        _ = Prompt.ask(
                            "Please install Rosetta by running `sudo softwareupdate --install-rosetta` in another terminal window.\nHit enter once complete and we will continue with the aws cli installation."
                        )
                        # Continues to prompt the user until the rosetta installation is found
                        while True:
                            rosetta_check = subprocess.run("pgrep -q oahd", shell=True)
                            if rosetta_check.returncode == 0:
                                rich.print(
                                    "[green]Rosetta has been installed successfully.[/green] Continuing with the aws cli installation."
                                )
                                break
                            else:
                                _ = Prompt.ask(
                                    "[red]Error: Rosetta installation still not found.[/red] Please run `sudo softwareupdate --install-rosetta` in another terminal window.\nHit enter once complete and we will continue with the aws cli installation."
                                )

                choices_xml_path = os.path.join(install_dir, "choices.xml")
                with open(choices_xml_path, "w") as f:
                    f.write(XML_TEMPLATE.format(install_dir=install_dir))
                install_sh = subprocess.run(
                    f"installer -pkg {file_path} -target CurrentUserHomeDirectory -applyChoiceChangesXML {choices_xml_path}",
                    shell=True,
                )
                if install_sh.returncode != 0:
                    rich.print(
                        f"[red]Error: failed to install aws, please run `installer -pkg {file_path} -target CurrentUserHomeDirectory -applyChoiceChangesXML choices.xml` in {install_dir}.[/red]."
                    )
                    return
                bin_dir = os.path.join(install_dir, "aws-cli")
            else:
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    zip_ref.extractall(install_dir)
                os.chmod(os.path.join(install_dir, "aws", "install"), 0o755)
                os.chmod(os.path.join(install_dir, "aws", "dist", "aws"), 0o744)
                bin_dir = os.path.join(install_dir, "bin")
                install_sh = subprocess.run(
                    f"./aws/install --install-dir {install_dir} --bin-dir {bin_dir}",
                    shell=True,
                    cwd=install_dir,
                )
                if install_sh.returncode != 0:
                    rich.print(
                        f"[red]Error: failed to install aws, please run `./aws/install --bin-dir {bin_dir}` in {install_dir}.[/red]."
                    )
                    return

            add_to_path = beaupy.confirm(
                "Would you like to add the `aws` binary to your PATH?",
                default_is_yes=True,
            )
            if add_to_path:
                if os.path.exists(os.path.expanduser("~/.bashrc")):
                    with open(os.path.expanduser("~/.bashrc"), "a") as f:
                        f.write(
                            f'\n# The next line updates PATH for the aws CLI.\nexport PATH="$PATH:{bin_dir}"\n'
                        )
                        f.write(
                            f'\n# The next line enables shell command completion for aws CLI.\ncomplete -C "{bin_dir}/aws_completer" aws\n'
                        )
                if os.path.exists(os.path.expanduser("~/.bash_profile")):
                    with open(os.path.expanduser("~/.bash_profile"), "a") as f:
                        f.write(
                            f'\n# The next line updates PATH for the aws CLI.\nexport PATH="$PATH:{bin_dir}"\n'
                        )
                        f.write(
                            f'\n# The next line enables shell command completion for aws CLI.\ncomplete -C "{bin_dir}/aws_completer" aws\n'
                        )
                if os.path.exists(os.path.expanduser("~/.zshrc")):
                    with open(os.path.expanduser("~/.zshrc"), "a") as f:
                        f.write(
                            f'\n# The next line updates PATH for the aws CLI.\nexport PATH="$PATH:{bin_dir}"\n'
                        )
                        f.write(
                            f'\n# The next line enables shell command completion for aws CLI.\ncomplete -C "{bin_dir}/aws_completer" aws\n'
                        )
            rich.print(
                "[green]`aws` CLI successfully installed. You will need to reload your terminal to use it.[/green]"
            )
            aws_bin = os.path.join(bin_dir, "aws")
        else:
            rich.print("[green]`aws` CLI is installed[/green]")
            aws_bin = "aws"
        process = subprocess.run(
            f"{aws_bin} sts get-caller-identity", shell=True, capture_output=True
        )
        if process.returncode != 0:
            rich.print("[red]Error: No default `aws` credentials found.[/red]")
            set_up_auth = beaupy.confirm(
                "Would you like us to authenticate for you?", default_is_yes=True
            )
            if set_up_auth:
                profile_name = beaupy.prompt(
                    "What profile name would you like to use (defaults to `LocalProfile`)?",
                    initial_value="LocalProfile",
                )
                use_sso = beaupy.confirm(
                    "Does your AWS account use AWS SSO? Hint: you would have a login URL like `https://<org_name>.awsapps.com/start`",
                    default_is_yes=False,
                )
                if use_sso:
                    rich.print(
                        f"Running:\n\n\t$ aws configure sso --profile {profile_name}\n\nYou will need to have your AWS SSO URL ready. Visit https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html for more information.\n"
                    )
                    process = subprocess.run(
                        f"{aws_bin} configure sso --profile {profile_name}", shell=True
                    )
                else:
                    rich.print(
                        f"Running:\n\n\t$ aws configure --profile {profile_name}\n\nYou will need to have your AWS access key ID and secret access key ready. Visit https://console.aws.amazon.com/iam/home#/security_credentials to create them.\nVisit https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html for more information.\n"
                    )
                    process = subprocess.run(
                        f"{aws_bin} configure --profile {profile_name}", shell=True
                    )
                set_default_profile = beaupy.confirm(
                    f"Would you like to set `{profile_name}` as your default AWS profile? (Recommended)",
                    default_is_yes=True,
                )
                if set_default_profile:
                    print(
                        f"Running:\n\n\t$ aws configure set default.profile {profile_name}\n"
                    )
                    process = subprocess.run(
                        f"{aws_bin} configure set default.profile {profile_name}",
                        shell=True,
                    )
                # TODO: Make sure this doesnt run on cntl+c
                rich.print(
                    f"[green]`aws` successfully authenticated with profile `{profile_name}`[/green]"
                )
        else:
            rich.print("[green]`aws` is authenticated[/green]")

    rich.print(
        "\n[i]Your local machine is setup to interact with AWS resources using LaunchFlow's Python SDK and/or the `aws` CLI.[/i]"
    )


async def _connect_aws(
    client: LaunchFlowAsyncClient,
    account_id: str,
    external_role_id: str,
    template_url: str,
):
    aws_account_id = Prompt.ask(
        "\nEnter your AWS account ID (can be found in the top right corner of https://console.aws.amazon.com/)."
    )

    print("\nSelect the AWS region you would like to setup LaunchFlow in:")
    region = beaupy.select(AWS_REGIONS, pagination=True)
    rich.print(f"[pink1]>[/pink1] {region}\n")

    url = _AWS_URL.format(
        region=region, external_id=external_role_id, template_url=template_url
    )
    webbrowser.open(url)
    rich.print(" - Visit the AWS Console to create a CloudFormation stack")
    rich.print(' - Scroll to the bottom and check the "I acknowledge..." box ')
    rich.print(
        ' - Click on "Create Stack". It may take a few minutes for the fole to be fully created.\n'
    )

    rich.print(
        "[i]This role will be used to provision AWS resources and deployments in your AWS account.[/i]\n"
    )

    _ = Prompt.ask(
        "Once the role is fully created hit enter to have us verify the setup"
    )

    # polls for a successful connection for up to 60 seconds
    start_time = time.time()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("Verifying AWS connection\n", total=None)

        done = False
        while not done:
            try:
                await client.connect.connect_aws(
                    account_id=account_id, aws_account_id=aws_account_id
                )
                done = True
            except LaunchFlowRequestFailure:
                if time.time() - start_time > 60:
                    raise TimeoutError(
                        "AWS setup verification timed out. Please try again."
                    )
            await asyncio.sleep(3)

        progress.remove_task(task)

    rich.print("\n[bold]AWS successfully connected[/bold] 🚀")

    _setup_local_aws_env()


def _setup_local_gcp_env(ask: bool = True):
    answer = True
    if ask:
        answer = beaupy.confirm(
            "Would you like us to verify your local GCP setup?", default_is_yes=True
        )
    if answer:
        process = subprocess.run("gcloud --version", shell=True, capture_output=True)
        if process.returncode == 127:
            rich.print("[red]Error: `gcloud` was not installed[/red].")
            install = beaupy.confirm(
                "Would you like to install it? (we will follow the steps outlined on https://cloud.google.com/sdk/docs/install)",
                default_is_yes=True,
            )
            if not install:
                return
            install_dir = beaupy.prompt(
                "Which directory would you like to install `gcloud` to (defaults to your home directory `~/gcloud`)?",
                initial_value="~/gcloud",
            )
            if install_dir == "~/gcloud":
                install_dir = os.path.expanduser(install_dir)
            system = platform.system()
            download_url = ""
            proc_type = ""
            if system == "Darwin":
                proc = subprocess.run("uname -m", shell=True, capture_output=True)
                proc_type = proc.stdout.decode("utf-8").strip()
                if proc.returncode != 0:
                    rich.print(
                        "[red]Error: failed to determine your processor type.[/red]."
                    )
                    return
                if proc_type == "arm64":
                    download_url = "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-470.0.0-darwin-arm.tar.gz"
                elif proc_type == "x86_64":
                    download_url = "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-470.0.0-darwin-x86_64.tar.gz"
                elif proc_type == "x86":
                    download_url = "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-470.0.0-darwin-x86.tar.gz"
                else:
                    rich.print(
                        f"[red]Error: Processor not supported: {proc_type}.[/red] You can manually install gcloud following the instructions at: https://cloud.google.com/sdk/docs/install#mac, please reach out to us at founders@launchflow.com to have us add support for your machine type."
                    )
                    return
            elif system == "Linux":
                proc_type = platform.machine()
                if proc_type == "x86_64":
                    download_url = "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-470.0.0-linux-x86_64.tar.gz"
                elif proc_type == "x86":
                    download_url = "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-470.0.0-linux-x86.tar.gz"
                elif proc_type == "arm64":
                    download_url = "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-470.0.0-linux-arm.tar.gz"
                else:
                    rich.print(
                        f"[red]Error: Processor not supported: {proc_type}[/red]. You can manually install gcloud following the instructions at: https://cloud.google.com/sdk/docs/install#linux, please reach out to us at founders@launchflow.com to have us add support for your machine type."
                    )
                    return
            else:
                # TODO: support windows
                rich.print(
                    f"[red]Error: OS not supported: {system}. You can manually install gcloud following the instructions at: https://cloud.google.com/sdk/docs/install[/red]"
                )
                return
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
            ) as progress:
                download_task = progress.add_task(
                    f"Downloading gcloud for {system} {proc_type}..."
                )
                response = requests.get(download_url, stream=True)
                if response.status_code != 200:
                    rich.print(
                        f"[red]Error: failed to download gcloud from: {download_url}.[/red]."
                    )
                    return
                tar_file = os.path.join(install_dir, "gcloud.tar.gz")
                os.makedirs(install_dir, exist_ok=True)
                with open(tar_file, "wb") as f:
                    f.write(response.raw.read())
                progress.remove_task(download_task)
                progress.console.print(
                    f"[green]✓[/green] Downloaded gcloud for {system} {proc_type}."
                )
            with tarfile.open(tar_file) as tar:
                # NOTE: This is deprecated but it is a trusted tarfile
                # provided by google.
                tar.extractall(install_dir)
            install_sh = subprocess.run(
                "./google-cloud-sdk/install.sh",
                shell=True,
                cwd=install_dir,
            )
            if install_sh.returncode != 0:
                rich.print(
                    f"[red]Error: failed to install gcloud, please run `./google-cloud-sdk/install.sh -q` in {install_dir}.[/red]."
                )
                return
            init_step = subprocess.run(
                "./google-cloud-sdk/bin/gcloud init",
                shell=True,
                cwd=install_dir,
            )
            if init_step.returncode != 0:
                rich.print(
                    f"[red]Error: failed to initialize gcloud, please run `./google-cloud-sdk/bin/gcloud init` in {install_dir}.[/red]."
                )
                return
            rich.print(
                "[green]`gcloud` successfully installed. You will need to reload your terminal to use it.[/green]"
            )
        else:
            rich.print("[green]`gcloud` is installed[/green]")

        check_auth = beaupy.confirm(
            "Would you like to check if you are authenticated with `gcloud`?",
            default_is_yes=True,
        )
        if check_auth:
            rich.print(
                "Checking local `gcloud` authentication. NOTE: Older versions of `gcloud` may prompt you for a password."
            )
            rich.print(
                "Running: \n\n\t$ gcloud auth application-default print-access-token\n\n"
            )
            process = subprocess.run(
                "gcloud auth application-default print-access-token",
                shell=True,
                capture_output=True,
                start_new_session=True,
            )
            if process.returncode != 0:
                rich.print("[red]Error: No default `gcloud` credentials found.[/red]")
                set_up_auth = beaupy.confirm(
                    "Would you like us to authenticate for you?", default_is_yes=True
                )
                if set_up_auth:
                    rich.print(
                        "Running:\n\n\t$ gcloud auth login --update-adc\n\nYou can run this whenever you need to reauthenticate your machine with GCP.\n"
                    )
                    process = subprocess.run(
                        "gcloud auth login --update-adc",
                        shell=True,
                        start_new_session=True,
                    )
            else:
                rich.print("[green]`gcloud` is authenticated[/green]")
        else:
            rich.print(
                "[i]Skipping gcloud auth check. You can run `gcloud auth login --update-adc` to authenticate with GCP.[/i]"
            )

    rich.print(
        "\n[i]Your local machine is setup to interact with GCP resources using LaunchFlow's Python SDK and/or the `gcloud` CLI.[/i]"
    )


async def _add_gcp_permissions(service_account: str):
    try:
        import googleapiclient.discovery
        from google.auth import exceptions
        from google.cloud import resourcemanager_v3
        from googleapiclient.errors import HttpError
    except ImportError:
        rich.print(
            "[red]Error: Ensure GCP dependencies are installed by running `pip install launchflow\[gcp]` to setup gcp.[/red]"
        )
        raise typer.Exit(1)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        try:
            task = progress.add_task("Looking up GCP organizations...", total=None)
            organization_client = resourcemanager_v3.OrganizationsAsyncClient()
            orgs_pager = await organization_client.search_organizations()
        except exceptions.DefaultCredentialsError:
            progress.remove_task(task)
            rich.print(
                "[red]Error: Default credentials not found. Set them up with `gcloud auth login --update-adc`[/red]"
            )
            raise typer.Exit(1)

        orgs = []
        prompts = []
        async for org in orgs_pager:
            orgs.append(org)
            prompts.append(f"{org.display_name} ({org.name})")
        progress.remove_task(task)
    if not orgs:
        rich.print(
            "[red]Error: no organizations found.[/red]\n\nVisit https://cloud.google.com/resource-manager/docs/creating-managing-organization to learn how to set this up.\n"
            "Please contact founders@launchflow.com if you would like help setting up your GCP organization."
        )
        raise typer.Exit(1)
    rich.print("Select the organization you would like to connect LaunchFlow to:")
    answer = beaupy.select(prompts, return_index=True, strict=True)
    rich.print(f"[pink1]>[/pink1] {prompts[answer]}\n")
    org = orgs[answer]
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(
            f"Connecting LaunchFlow to `{org.display_name}`...", total=None
        )

        # Ensures the Organization has a billing account, and prompts the user to select one if not
        billing_service = googleapiclient.discovery.build("cloudbilling", "v1")
        req = billing_service.organizations().billingAccounts().list(parent=org.name)
        response = req.execute()
        billing_accounts = response.get("billingAccounts", [])
        if not billing_accounts:
            rich.print(
                f"[red]Error: No billing account attached to Org `{org.display_name}`.[/red]"
            )
            # First we list all the billing accounts the user has access to
            req = billing_service.billingAccounts().list()
            response = req.execute()
            billing_accounts = response.get("billingAccounts", [])
            if not billing_accounts:
                rich.print(
                    "[red]Error: No billing accounts found for the current Google user.[/red]\n"
                    "Visit https://console.cloud.google.com/billing to create a billing account.\n\nPlease contact founders@launchflow.com if you need help setting up GCP billing."
                )
                raise typer.Exit(1)

            if len(billing_accounts) == 1:
                billing_account = billing_accounts[0]
                answer = beaupy.confirm(
                    f"Would you like to use the billing account `{billing_account['displayName']}`?",
                    default_is_yes=True,
                )
                if not answer:
                    rich.print(
                        "[red]Error: No billing account selected - Exiting.[/red]\n\nPlease contact founders@launchflow.com if you need help setting up GCP billing."
                    )
                    raise typer.Exit(1)
            else:
                rich.print("Select the billing account you would like to use:")
                prompts = [
                    f"{ba['displayName']} ({ba['name']})" for ba in billing_accounts
                ]
                answer = beaupy.select(prompts, return_index=True, strict=True)
                rich.print(f"[pink1]>[/pink1] {prompts[answer]}\n")
                billing_account = billing_accounts[answer]

            while True:
                try:
                    policy = (
                        billing_service.billingAccounts()
                        .getIamPolicy(resource=billing_account["name"])
                        .execute()
                    )
                    bindings = policy.get("bindings", [])
                    for role in ["roles/billing.user"]:
                        bindings.append(
                            {
                                "role": role,
                                "members": [f"serviceAccount:{service_account}"],
                            }
                        )
                    policy["bindings"] = bindings
                    billing_service.billingAccounts().setIamPolicy(
                        resource=billing_account["name"], body={"policy": policy}
                    ).execute()
                    break
                except HttpError as e:
                    if e.status_code == 409:
                        # NOTE: this can happen sometimes when a concurrent policy modification
                        # happens, we just retry in this case after waiting a bit.
                        await asyncio.sleep(2)
                        continue
                    rich.print(
                        f"[red]Error: failed to add permissions to billing account: {e}[/red]"
                    )
                    typer.Exit(1)
            progress.console.print(
                f"[green]✓[/green] Permissions added to `{billing_account['displayName']}`."
            )

        while True:
            try:
                service = googleapiclient.discovery.build(
                    "cloudresourcemanager", "v1"
                ).organizations()
                get_request = service.getIamPolicy(resource=org.name)
                policy = get_request.execute()
                bindings = policy.get("bindings", [])
                for role in [
                    "roles/resourcemanager.folderCreator",
                    "roles/resourcemanager.organizationViewer",
                    "roles/billing.user",
                ]:
                    bindings.append(
                        {
                            "role": role,
                            "members": [f"serviceAccount:{service_account}"],
                        }
                    )
                policy["bindings"] = bindings
                set_request = service.setIamPolicy(
                    resource=org.name, body={"policy": policy}
                )
                set_request.execute()
                break
            except HttpError as e:
                if e.status_code == 409:
                    # NOTE: this can happen sometimes when a concurrent policy modification
                    # happens, we just retry in this case after waiting a bit.
                    await asyncio.sleep(2)
                    continue
                rich.print(f"[red]Error: failed to add permissions: {e}[/red]")
                typer.Exit(1)
        progress.console.print(
            f"[green]✓[/green] Permissions added to `{org.display_name}`."
        )
        progress.remove_task(task)


async def _connect_gcp(
    client: LaunchFlowAsyncClient,
    account_id: str,
    service_account_email: str,
    add_permissions: bool,
):
    if add_permissions:
        rich.print(
            f"\n`[cyan]{service_account_email}[/cyan]` needs the following roles on your GCP organization:"
        )
        rich.print("- Folder Creator ([i]roles/resourcemanager.folderCreator[/i])")
        rich.print(
            "- Organization Viewer ([i]roles/resourcemanager.organizationViewer[/i])"
        )
        rich.print("- Billing Account User ([i]roles/billing.user[/i])\n")

        rich.print(
            "[i]These roles will be used to create a unique GCP project for every environment in your account.[/i]\n"
        )

        rich.print("How would you like to add these roles?")
        options = [
            "Have LaunchFlow add them using my local credentials",
            "Manually add these roles via the GCP console",
        ]
        answer = beaupy.select(options, strict=True, return_index=True)
        rich.print(f"[pink1]>[/pink1] {options[answer]}")
        if answer == 0:
            rich.print("Verifying local GCP setup...")
            _setup_local_gcp_env(ask=False)
            await _add_gcp_permissions(service_account_email)
        else:
            _ = Prompt.ask("Hit enter once complete and we will verify your setup")
    # polls for a successful connection for up to 60 seconds
    start_time = time.time()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(
            "Verifying GCP connection (this may take a minute)...\n", total=None
        )

        done = False
        while not done:
            try:
                await client.connect.connect_gcp(account_id=account_id)
                done = True
            except LaunchFlowRequestFailure as e:
                if e.status_code == 409:
                    progress.remove_task(task)
                    rich.print(
                        f"[red]Error: GCP verification failed: {e}[/red]\n\nPlease contact founders@launchflow.com if you need help connecting your account to GCP."
                    )
                    raise typer.Exit(1)
                elif e.status_code == 422:
                    progress.remove_task(task)
                    rich.print(f"[red]Error: GCP verification failed: {e}[/red]")
                    # ask if they'd like to retry
                    retry = beaupy.confirm(
                        "Would you like us to add the permissions and retry the connection?",
                        default_is_yes=True,
                    )
                    if retry:
                        progress.stop()
                        await _connect_gcp(
                            client,
                            account_id,
                            service_account_email,
                            add_permissions=True,
                        )
                        return
                    else:
                        raise typer.Exit(1)
                if time.time() - start_time > 60:
                    raise TimeoutError(
                        "GCP setup verification timed out. Please try again."
                    )
            await asyncio.sleep(3)

        progress.remove_task(task)

    rich.print("[bold]GCP successfully connected[/bold] 🚀\n")

    _setup_local_gcp_env()
    rich.print(
        "[i]You can now create environments and deploy resources to your GCP account using LaunchFlow.[/i]"
    )
