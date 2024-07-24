
## `git-vars` - Manage GitLab Environment Variables with Ease
  

**`git-vars`** is a Python package that simplifies managing GitLab environment variables. It allows you to seamlessly synchronize environment variables between your local machine and GitLab projects. This streamlines your development workflow by ensuring consistency and eliminating the hassle of manual updates.

  

## Installation

  

Install `git-vars` using pip:

  

```bash

pip install  git-vars

```

## Usage

`git-vars` offers two main subcommands: `pull` and `push`.

  

## Pull

Use the pull command to retrieve environment variables from your GitLab project and store them in a local file.

  

```Bash

git-vars pull  -t <access_token> -r <repository_url> [options]

```

  

**Options**:

  

`-t`, `--access-token`: (Optional) Your GitLab personal access token with sufficient permissions to access environment variables. If not provided, git-vars will check the environment variable GITLAB_VARIABLE_ACCESS_TOKEN for the token.

  

`-r`, `--repository-url`: (Optional) The URL of your GitLab repository. If not provided, git-vars will check the environment variable GITLAB_REPOSITORY_URL for the repository URL.

  

`-s`, `--scope`: (Optional) The scope of environment variables to pull. Valid options are project (default), group, or instance.
 If not provided, git-vars will check the environment variable GITLAB_PROJECT_SCOPE for the scope. If there is not environment variable, will take 'project' as default. 
  

`-f`, `--file`: (Optional) Path to the file where downloaded variables will be saved. Defaults to `.env`.

  

## Push

Use the push command to update GitLab environment variables from a local file.

  

```Bash

git-vars push  -t <access_token> -r <repository_url> [options]


```

  

**Options**:

  

`-t`, `--access-token`: (Optional) Your GitLab personal access token with sufficient permissions to access environment variables. If not provided, git-vars will check the environment variable GITLAB_VARIABLE_ACCESS_TOKEN for the token.

  

`-r`, `--repository-url`: (Optional) The URL of your GitLab repository. If not provided, git-vars will check the environment variable GITLAB_REPOSITORY_URL or GITLAB_PROJECT_SCOPE (depending on the scope) for the repository URL.

  

`-s`, `--scope`: (Optional) The scope of environment variables to pull. Valid options are project (default), group, or instance.
 If not provided, git-vars will check the environment variable GITLAB_PROJECT_SCOPE for the scope. If there is not environment variable, will take 'project' as default. 

  

`-f`, `--file`: Path to the file containing environment variables to push. Defaults to `.env`.

  

Example:

  

Pull project environment variables from your GitLab repository and save them to a file named my_env.txt:

```Bash

git-vars pull  -t  your_access_token  -r  https://gitlab.com/username/project-name  -f  .env


```

  

Push environment variables defined in local_env.env to your GitLab project's group environment variables:

```Bash

git-vars push  -t  your_access_token  -r  https://gitlab.com/username/group-name  -s  group  -f  local_env.env

```

  

## Additional Notes

Make sure you have a personal access token with the necessary permissions created in your GitLab account.

Environment variables are stored in a standard .env file format on your local machine (configurable with -f or --file).

For detailed information on specific functionalities and error handling, refer to the source code within the package.

  

## Contributing

We welcome contributions to improve this project. Please refer to the Contributing Guide (if available) for details on how to submit pull requests and participate in development.
