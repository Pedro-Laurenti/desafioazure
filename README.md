# Desafio Azure Functions

Este projeto contém duas funções Azure Functions em Python, desenvolvidas para atender aos requisitos do desafio proposto pela [Accenture](https://www.accenture.com/br-pt).

## Estrutura do Projeto

- **Function1 (Time Trigger)**: Coleta dados de uma URL específica e os salva em um container do Blob Storage.
- **Function2 (HTTP Request)**: Recebe um valor de taxa em formato JSON e salva um arquivo XML no Blob Storage.

## Funcionalidades

### 1. Time Trigger

- **Descrição**: Esta função é executada automaticamente entre 18:40 e 19:30 em dias de semana.
- **URL de Coleta**: `https://sistemaswebb3-balcao.b3.com.br/featuresDIProxy/DICall/GetRateDI/eyJsYW5ndWFnZSI6InB0LWJyIn0=`
- **Armazenamento**: O JSON coletado é salvo em um container específico no Blob Storage.

**Arquitetura** - A função verifica a data do JSON retornado e evita coletar dados novamente se já tiver coletado para a data atual.

### 2. HTTP Request

- **Descrição**: Recebe uma requisição com o conteúdo `{"rate":"10,65"}`.
- **Formato de Saída**: Salva um arquivo XML no formato `<xml><rate value="10.65"></rate></xml>` em um container no Blob Storage.

**Arquitetura** - Utiliza uma fila para gerenciar requisições que possam resultar em timeout. Mesmo se a função exceder o tempo limite, o processamento será retomado a partir da fila.

## Como Testar

### Testando Localmente

Para rodar as funções localmente, siga os passos abaixo:

1. **Configuração Local**:

   - Certifique-se de que o [Azure Functions Core Tools](https://docs.microsoft.com/azure/azure-functions/functions-run-local) e o Python estão instalados.
   - No terminal, navegue até o diretório do projeto e execute `func start` para iniciar as funções localmente.
2. **Testando a Função Time Trigger**:

   - Simule a execução da função Time Trigger alterando o cronograma para uma frequência mais curta (por exemplo, a cada minuto).
   - Verifique no console do Azure Functions Core Tools se a função executa corretamente.
   - Confirme que o JSON é salvo em seu Blob Storage, acessando o portal do Azure e navegando até seu container.
3. **Testando a Função HTTP Request**:

   - Use o Postman ou cURL para enviar uma requisição `POST` local:
     - **URL**: `http://localhost:7071/api/HttpRequestFunction`
     - **Body** (JSON):
       ```json
       {"rate": "10,65"}
       ```
   - Após enviar a requisição, confirme se o arquivo XML foi criado no Blob Storage.

### Testando na Aplicação Web

A aplicação web está hospedada no Azure e disponível até **15 de novembro** de 2024. Acesse a aplicação em: [https://desafioazure2.azurewebsites.net](https://desafioazure2.azurewebsites.net).

1. **Função HTTP Request na Web**:
   - Envie uma requisição `POST` para a URL:
     ```
     https://desafioazure2.azurewebsites.net/api/HttpRequestFunction
     ```
   - Utilize o corpo JSON:
     ```json
     {"rate": "10,65"}
     ```
   - Verifique se você recebe uma resposta `200 OK` indicando sucesso.
   - Acesse o Blob Storage no portal do Azure para confirmar que o arquivo XML foi criado.

### Verificação de Logs e Execuções

Para monitorar a execução das funções e ver logs de erros, se houver:

1. No **Portal do Azure**, vá para **Function App**.
2. Acesse a função específica e clique em **Monitor** para ver o histórico de execuções e logs detalhados.

## URLs Importantes

- Aplicação Web: [https://desafioazure2.azurewebsites.net](https://desafioazure2.azurewebsites.net)
- Repositório do Projeto: [https://github.com/Pedro-Laurenti/desafioazure](https://github.com/Pedro-Laurenti/desafioazure)

## Considerações Finais

Este projeto foi desenvolvido para demonstrar o uso de Azure Functions com Python e a interação com Blob Storage. Para mais informações, consulte a [documentação oficial da Microsoft](https://docs.microsoft.com/azure/azure-functions/).

## Contato

Para dúvidas ou sugestões, entre em contato.
