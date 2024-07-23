# Codenrock CLI

CLI для управления моделями ML на платформе Codenrock.

## Создание виртуальной среды
```sh
python3 -m venv venv
source venv/bin/activate
```

## Установка

```sh
pip install codenrock
```

## Использование

```sh
codenrock login --email='your_email@example.com'
codenrock 'team list'
codenrock 'model create' --name "Model Name" --description "Model Description" --path='/path/to/model'  --team_id='227'
codenrock 'model update' --id "model_id" --name "New Model Name" --description "New Description" --path "/path/to/new/model"
codenrock 'model delete' --id "model_id"
codenrock 'model list'
codenrock 'model show' --id "model_id"

```
