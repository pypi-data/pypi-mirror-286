from ..model_framework import ModelFramework, ModelFrameworkType


class Custom(ModelFramework):
    framework_name: str = "custom"
    additional_requirements: list = ["numpy", "joblib"]
    requirements: list = [framework_name]

    def typ(self) -> ModelFrameworkType:
        return ModelFrameworkType.CUSTOM

    def supports_model_class(self, model_class) -> bool:
        # model_framework, _, _ = model_class.__module__.partition(".")
        # return model_framework == ModelFrameworkType.CUSTOM.value

        return True

    def get_requirements(self):
        # print('Inside sklearn  get_requirements')

        # default_requirements = [infer_requirements(framework_name=self.framework_name)]

        # self.requirements = default_requirements + self.additional_requirements
        self.requirements = self.additional_requirements

        return self.requirements
