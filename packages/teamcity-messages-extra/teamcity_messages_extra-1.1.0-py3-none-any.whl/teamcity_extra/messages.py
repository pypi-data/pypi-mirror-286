from teamcity.messages import TeamcityServiceMessages as _TSM

NO_OUTPUT = object()


class TeamcityServiceMessages(_TSM):
    def testMetadata(self, testName, name, value='', type='', flowId=None):
        # https://www.jetbrains.com/help/teamcity/reporting-test-metadata.html#Reporting+Additional+Test+Data
        self.message('testMetadata', name=name, testName=testName, value=value, type=type, flowId=flowId)

    def buildStatisticValue(self, key, value):
        # https://www.jetbrains.com/help/teamcity/service-messages.html#Reporting+Build+Statistics
        self.message('buildStatisticValue', key=key, value=str(value))

    def addBuildTag(self, tag):
        # https://www.jetbrains.com/help/teamcity/service-messages.html#Adding+and+Removing+Build+Tags
        self._single_value_message('addBuildTag', tag)

    def removeBuildTag(self, tag):
        # https://www.jetbrains.com/help/teamcity/service-messages.html#Adding+and+Removing+Build+Tags
        self._single_value_message('removeBuildTag', tag)

    def message(self, messageName, **properties):
        if self.output == NO_OUTPUT:
            return
        return super().message(messageName, **properties)

    def _single_value_message(self, messageName, value):
        if self.output == NO_OUTPUT:
            return
        return super()._single_value_message(messageName, value)
