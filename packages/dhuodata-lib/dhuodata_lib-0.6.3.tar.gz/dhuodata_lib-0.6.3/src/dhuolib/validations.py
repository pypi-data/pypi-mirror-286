from pydantic import BaseModel, Field, field_validator


class ModelBody(BaseModel):
    modelname: str = Field(..., description="Model Name")
    tags: dict = Field(None, description="Tags")
    stage: str = Field(..., description="STAGING|PRODUCTION")
    run_id: str = Field(..., description="Run ID")
    model_uri: str = Field(..., description="Model URI")

    @field_validator("modelname", "stage", "run_id", "model_uri")
    def validate_empty_values(cls, value):
        if value == "":
            raise ValueError("Value cannot be empty")
        return value


class RunExperiment(BaseModel):
    type_model: str = Field(
        ..., description="RANDOM_FOREST|XGBOOST|LINEAR_REGRESSION|LOGISTIC_REGRESSION"
    )
    experiment_name: str = Field(..., description="Experiment Name")
    tags: dict = Field(None, description="Tags")

    @field_validator("type_model", "experiment_name")
    def validate_empty_values(cls, value):
        if value == "":
            raise ValueError("Value cannot be empty")
        return value


class RunFiles(BaseModel):
    modelpkl_path: str = Field(..., description="Path to model.pkl")
    requirements_path: str = Field(..., description="Path to requirements.txt")

    @field_validator("modelpkl_path", "requirements_path")
    def validate_empty_values(cls, value):
        if value == "":
            raise ValueError("Value cannot be empty")
        return value


class ExperimentBody(BaseModel):
    experiment_name: str = Field(..., description="Id")
    experiment_tags: dict = Field(None, description="Tags")


class PredictOnlineModelBody(BaseModel):
    run_id: str = Field(None, description="Run ID")
    modelname: str = Field(..., description="DEPENDENCY|PREDICT")
    stage: str = Field(..., description="STAGING|PRODUCTION")

    @field_validator("modelname", "stage")
    def validate_empty_values(cls, value):
        if value == "":
            raise ValueError("Value cannot be empty")
        return value


class PredictBatchModelBody(BaseModel):
    run_id: str = Field(None, description="Run ID")
    modelname: str = Field(..., description="DEPENDENCY|PREDICT")
    stage: str = Field(..., description="STAGING|PRODUCTION")
    batch_model_dir: str = Field(..., description="Batch File")
    experiment_name: str = Field(..., description="Experiment Name")
    type_model: str = Field(
        ..., description="RANDOM_FOREST|XGBOOST|LINEAR_REGRESSION|LOGISTIC_REGRESSION"
    )

    @field_validator(
        "modelname", "stage", "batch_model_dir", "experiment_name", "type_model"
    )
    def validate_empty_values(cls, value):
        if value == "":
            raise ValueError("Value cannot be empty")
        return value


class ConnectModel(BaseModel):
    dialect_drive: str = Field(..., description="Dialect")
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")
    host: str = Field(..., description="Host")
    port: str = Field(..., description="Port")
    service_name: str = Field(..., description="Service Name")

    @field_validator(
        "dialect_drive", "username", "password", "host", "port", "service_name"
    )
    def validate_empty_values(cls, value):
        if value == "":
            raise ValueError("Value cannot be empty")
        return value


class TransitionModel(BaseModel):
    model_name: str = Field(..., description="Model Name")
    version: str = Field(..., description="Version")
    stage: str = Field(..., description="STAGING|PRODUCTION")

    @field_validator("model_name", "stage")
    def validate_empty_values(cls, value):
        if value == "":
            raise ValueError("Value cannot be empty")
        return value


class RunSearch(BaseModel):
    filter_string: str = Field(None, description="Filter String")
    max_results: int = Field(None, description="Max Results")
    page_token: str = Field(None, description="Page Token")
    experiment_name: str = Field(..., description="Experiment Name")

    @field_validator("filter_string", "experiment_name")
    def validate_empty_values(cls, value):
        if value == "":
            raise ValueError("Value cannot be empty")
        return value
