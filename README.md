# `ragna-aws`

AWS extensions for [Ragna](https://ragna.chat). Currently supports

- [AWS S3](https://aws.amazon.com/s3/) as `ragna.core.Document`
- [AWS Bedrock](https://aws.amazon.com/bedrock/) as `ragna.core.Assistant`s

## Installation

```shell
$ pip install ragna-aws
```

## Usage

Put the following, or a subset thereof, into your Ragna configuration file, e.g.
`ragna.toml`:

```toml
# ...

[core]
# ...
document = "ragna_aws.S3Document"
assistants = [
    # ...
    "ragna_aws.Claude",
    "ragna_aws.ClaudeInstant",
    "ragna_aws.Command",
    "ragna_aws.CommandLight",
    "ragna_aws.Jurassic2Mid",
    "ragna_aws.Jurassic2Ultra",
    "ragna_aws.Llama2Chat13B",
    "ragna_aws.Llama2Chat70B",
    "ragna_aws.TitanTextExpress",
    "ragna_aws.TitanTextLite",
]
```
