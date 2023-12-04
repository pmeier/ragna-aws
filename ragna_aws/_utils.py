from ragna.core import EnvVarRequirement


# FIXME: Instead of depending on env vars here, users can also supply this through
#  a credentials file. Plus, when inside AWS, i.e. in a deployment, these can be
#  auto-detected.
class AwsRequirement(EnvVarRequirement):
    pass


AWS_ACCESS_KEY_ID_REQUIREMENT = AwsRequirement("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY_REQUIREMENT = AwsRequirement("AWS_SECRET_ACCESS_KEY")
AWS_REGION_REQUIREMENT = AwsRequirement("AWS_DEFAULT_REGION")


AWS_DEFAULT_REQUIREMENTS = [
    AWS_ACCESS_KEY_ID_REQUIREMENT,
    AWS_SECRET_ACCESS_KEY_REQUIREMENT,
    AWS_REGION_REQUIREMENT,
]
