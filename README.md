# DBCChecker

> A prototype tool aiming to verify security properties of systems obtained by composition of containers.

## How to run

In order to run the system execute

    docker compose up --build

in the main directory. On older systems where `compose` is not included with `docker`, use `docker-compose`.

## GUI

The GUI offered in the releases is a prototype that aims to simplify the interaction with the REST API.

To execute it you need Java (>=14):

    java -jar serverProverifGui-1.1.0-${PLATFORM}-STANDALONE.jar

where `${PLATFORM}` is either `LINUX` or `WINDOWS` based on your platform.

## Pre-built Docker images

In the releases you can also find pre-built docker images. To import them you can use `docker load`.

## Examples

- **basicReplyAttack**: it represents a vulnerable system, where a reply attack is discovered
- **dataLeakage**: this example represents the situation where a **safe system**, after a composition with a another container, loses the desired security properties.

## API List

You can use DBCChecker without the GUI, calling directly the following APIs:

- **GET - Models List**: Get a list with all the models.

    <http://localhost:8080/models>

- **GET - Model**: Get a list with the name of all model's files.

    <http://localhost:8080/models/{model-name}>

- **POST - Model**: Create a new model and all the subdirectory related to it.

    <http://localhost:8080/models/{model-name}>

- **DELETE - Model**: Delete a model with all the files related.

    <http://localhost:8080/models/{model-name}>

- **GET - Input File**: Get an input file of a particular model.

    <http://localhost:8080/models/{model-name}/input/text/{file-name}>

- **POST - Input File** (ProVerif): Post the input file of a choosen model.

    <http://localhost:8080/models/{model-name}/input/text/{file-name}>

    | Body Key | Description|
    | --- | --- |
    | DataProverif | ProVerif File represent the model to verify |

- **POST - Input File** (JSON): Create the input file of a choosen model from JBF.

    <http://localhost:8080/models/{model-name}/input/text/{file-name}>

    | Body Key | Description|
    | --- | --- |
    | DataJsonBigraph | JBF File represent the model to verify |
    | DataJsonIntegrative | JBF Integrative File |

- **PUT - Input File** (ProVerif): Update the input file of a choosen model.

    <http://localhost:8080/models/{model-name}/input/text/{file-name}>

    | Body Key | Description|
    | --- | --- |
    | DataProverif | ProVerif File represent the model to verify |

- **PUT - Input File** (JSON): Update the input file of a choosen model from JBF.

    <http://localhost:8080/models/{model-name}/input/text/{file-name}>

    | Body Key | Description|
    | --- | --- |
    | DataJsonBigraph | JBF File represent the model to verify |
    | DataJsonIntegrative | JBF Integrative File |

- **DELETE - Input file**: Delete the input file of a choosen model.

    <http://localhost:8080/models/{model-name}/input/text/{file-name}>

- **POST - Verify**: Verify the input file with ProVerif and save the result.

    <http://localhost:8080/models/{model-name}/verify/{file-name}>

    | Body Key | Description|
    | --- | --- |
    | VerificationType | both / text / html |
    | DataJsonBigraph | JBF File represent the model to verify |
    | DataJsonIntegrative | JBF Integrative File |

- **PUT - Verify**: Update the verification of the input file with ProVerif and save the result.

    <http://localhost:8080/models/{model-name}/verify/{file-name}>

    | Body Key | Description|
    | --- | --- |
    | VerificationType | both / text / html |
    | DataJsonBigraph | JBF File represent the model to verify |
    | DataJsonIntegrative | JBF Integrative File |

- **GET - Output Text**: Get the standard ProVerif output file of a choosen model.

    <http://localhost:8080/models/{model-name}/output/text/{file-name}>

- **DELETE - Output Text**: Delete the standard ProVerif output file of a choosen model.

    <http://localhost:8080/models/{model-name}/output/text/{file-name}>

- **GET - Output Text**: Get the html representation ProVerif output file of a choosen model.

    <http://localhost:8080/models/{model-name}/output/html/{file-name}>

- **DELETE - Output Text**: Delete the html representation ProVerif output file of a choosen model.

    <http://localhost:8080/models/{model-name}/output/html/{file-name}>
