## Release of V0.2.0
### Changes
- Added node-type based colouring for data lineage


## Release of V0.2.0
### Changes
- Removed projects. There will be no project related actions(creation, deletion etc.) in PureML
- `project.init()` equivalent for datasets is `dataset.init()`. This will create an empty an empty Dataset that will contain all the information about a dataset like **ReadME.md**, **branches**, **versions**, **reviews** etc
- - Each dataset registered using `@dataset` will be assigned a version 
- `project.init()` equivalent for models is `model.init()`. This will create an empty an empty Model that will contain all the information about a dataset like **ReadME.md**, **branches**, **versions**, **reviews** etc
- - Each model registered using `@model` will be assigned a version
- Added branching for datasets, and models





## Release of V0.1.6
### Changes
- Added support for more input types for fastAPI and Docker container
- Input types:
    - Numpy Ndarray
    - Pandas DataFrame
    - text
    - Image
- Output types:
    - Numpy Ndarray
    - Pandas DataFrame
    - text
    - Any json serializable output

### Bug fixes
- Building docker images without cache to utilize modified files
- Remove duplicate edges between two nodes in the data lineage
    

## Release of V0.1.5


## Release of V0.1.4
### Changes
- Added templates for bug report, feature request
- Added source code extraction
- Added support for creating FastAPI server for a model
- Added support for creating Docker container for a model
### Bug fixes
- Bug fix related to unconnected node when parent is not given in leange


## Release of V0.1.3
### Changes
- Added support for pytorch tabnet for model packaging
- Added ReadMe file to enable collaboration guidelines for PureML repository


### Bug fixes
- Bug fix related to missing packages
- Bug fix to generate nodes given in parents parameter of the decorators if they are not already available.


## Release of V0.1.2
### Changes

#### Decorators
- Added `model` decorator for registering dataset.
- Added `dataset` for registering dataset.
- Added `load_data` and `transformer` decorators for generating and registering data pipeline along with `dataset` decorator.

#### Project
- Project details can now be fetched by project name or id.

#### Data pipeline
- Data pipelines can be generated using decorators.
- The nodes contain `load_data`, `transformer` and `dataset`. 
    - `load_data` nodes are intended to be used to capture functionality that loads the data into memory. 
    - `transformer` nodes are intended to be used to capture functionality that does transformations on the loaded data.
    - `dataset` node is intended to be used to capture functionality that generate processed data.
- Every function that has a decorator can also specify its parent node/nodes. These parent nodes are utilized in generating an accurate data pipeline.

#### Versioning
- Added dataset registration to a project.
- Added pipeline generation and registration for a dataset.
- Added versioning of datasets, and models. Any model or dataset can be fetched by its name its associated version.


#### Logging
- Added `log` functionality to add metrics, params with ease.
- Logging of metrics/params can be done inside a `model` decorator without additional parameters of `model name` and `model version`. These parameters will be obtained from the model decorator.
- By default, metrics/params will be added to the `latest` version of model if no version is specified will logging.


## Release of V0.1.1
### Changes

- Added description
- Updated python support from ^3.10 to ^3.8
- Added docs for quick start
- Added dataset api's:  adding, delete, fetch, details
- Added decorators for model, dataset
- Removed organization details for signup
- Added versions for models. 
- Changed apis to take model version in calling

### Bug fixes
- Minor bug fixes in artifact details api
- Minor bug fix in backend base url
- Minor bug fix in signup api
- Minor bug fix in package requirements



## Release of V0.1.0

We have released version 0.1.0. We now support different components of the model registry. Here is the list of actionable items that are supported in the release version.


- Projects:
    - create: Create a new project
    - list: List existing projects created by a user
    - details: Fetch details for an existing project
    - clone: Clone an existing project and set it as current project
- Models:
    - register: Register a production ready model(in-memory) to the remote model registry
    - fetch: Fetch any model from the model registry as python object
    - list: List all the registered models under a project
    - details: Fetch details for an existing model
    - delete: Delete a model from the model registry
- Metrics:
    - add: Add metrics obtained for a model
    - fetch: Fetch the metrics added for a model. To obtain selective metrics, a key has to be passed
    - delete: Delete an added metric
- Params:
    - add: Add params related to a model
    - fetch: Fetch the params added for a model. To obtain selective params, a key has to be passed
    - delete: Delete an added param
- Artifacts:
    - add: Add artifacts for a registered model. 
    - details: Obtain the details for the added artifacts. 
    - fetch: Fetch the added artifacts. Fetched artifacts will be stored in local disk
    - delete: Delete the added artifacts