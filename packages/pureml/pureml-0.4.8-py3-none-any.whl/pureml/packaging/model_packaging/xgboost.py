from ..model_framework import ModelFramework, ModelFrameworkType
from ..packaging_utils import infer_requirements


class XGBoost(ModelFramework):
    framework_name: str = "xgboost"
    additional_requirements: list = ["numpy", "joblib"]
    requirements: list = [framework_name]

    def typ(self) -> ModelFrameworkType:
        return ModelFrameworkType.XGBOOST

    def supports_model_class(self, model_class) -> bool:
        model_framework, _, _ = model_class.__module__.partition(".")
        return model_framework == ModelFrameworkType.XGBOOST.value

    def get_requirements(self):
        # print('Inside sklearn  get_requirements')

        default_requirements = [infer_requirements(framework_name=self.framework_name)]

        self.requirements = default_requirements + self.additional_requirements

        return self.requirements
