# teamcity-messages-extra

![license](https://img.shields.io/badge/License-MIT-blue.svg)
[![tests](https://github.com/fopina/teamcity-messages-extra/workflows/tests/badge.svg)](https://github.com/fopina/teamcity-messages-extra/actions?query=workflow%3Atests)
[![Current version on PyPi](https://img.shields.io/pypi/v/teamcity-messages-extra)](https://pypi.org/project/teamcity-messages-extra/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/teamcity-messages-extra)

[teamcity-messages](https://pypi.org/project/teamcity-messages/) ([JetBrains official package](https://github.com/JetBrains/teamcity-messages/)) has no activity for over one year.

This package will try to address some of the missing features by extending official one. It's not a fork, [teamcity-messages](https://pypi.org/project/teamcity-messages/) is an actual dependency so that any dependency analysis tools (eg, [dependency-check](https://owasp.org/www-project-dependency-check/)) properly identify it.

## Usage

Just import `teamcity_extra` instead of `teamcity`. Everything from the official package will be available, plus the `extra`.

Instead of:
```python
from teamcity.messages import TeamcityServiceMessages
```
Use:
```python
from teamcity_extra.messages import TeamcityServiceMessages
```

## Extra

### TeamcityServiceMessages.testMetadata

[testMetadata service message](https://www.jetbrains.com/help/teamcity/reporting-test-metadata.html#Reporting+Additional+Test+Data)

### TeamcityServiceMessages.buildStatisticValue

[buildStatisticValue service message](https://www.jetbrains.com/help/teamcity/service-messages.html#Reporting+Build+Statistics)

### TeamcityServiceMessages.addBuildTag

[addBuildTag service message](https://www.jetbrains.com/help/teamcity/service-messages.html#Adding+and+Removing+Build+Tags)

### TeamcityServiceMessages.addBuildTag

[removeBuildTag service message](https://www.jetbrains.com/help/teamcity/service-messages.html#Adding+and+Removing+Build+Tags)

### TeamcityServiceMessages.NO_OUTPUT

[NO_OUTPUT output](https://github.com/fopina/teamcity-messages-extra/pull/7) will make all service message calls / methods in `TeamcityServiceMessages` to not print anything.

This allows for simpler code when teamcity output is optional

```python
from teamcity_extra.messages import TeamcityServiceMessages, NO_OUTPUT

# None is the default value (stdout)
tsm = TeamcityServiceMessages(output=None if should_report_to_teamcity() else NO_OUTPUT)

with tsm.test('thisTest'):
    doWhatever()
```
