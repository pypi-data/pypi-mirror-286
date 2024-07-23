# How to set up

```
docker compose -f ./Docker/docker-compose.yaml up --build -d
```

```
docker exec -it momiji bash
```

# アップロード方法

必要な編集が終わったら，まずは test から実行する．

## test

```git add .
poetry run pytest -v
```

を実行すると，`tests`にあるテストが実行される．その結果を見て問題がなければ次に進む．

## install

次に

```
poetry install
```

を実行して Python に自作ライブラリをインストールする．

## build

```
poetry build
```

とすると，publish に必要なファイル群が生成される．

## publish

Publish に必要な情報を入力する．

```
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi {Test PyPIのAPI Token}
poetry publish -r testpypi
```

とするとこで，Test PyPI にパッケージをアップロードできる．

```
poetry config pypi-token.pypi {PyPIのAPI Token}
poetry publish
```

とするとこで，PyPI にパッケージをアップロードできる．

# このリポジトリのブランチ

以下の順序でマージしていく
main←staging←dev

一人がプルリクをチェックしてマージ
dev_XXX で開発・プロジェクト管理

連動させる
staging : testpypi
main : pypi

base
テンプレートとして、ベースとなるこのリポジトリを取り込むため
(template が更新され、別のプロジェクトもその変更を取り入れたいとき、base ブランチにフェッチして取り込んで、dev にマージする)
→ このリポジトリは、常に main と base が同等にないといけない。(開発用のライブラリ用のリポジトリは全然違くて良い。出発点だけ揃える。)

参考 : [Github branch](https://scrapbox.io/openaging/Github_branch)
