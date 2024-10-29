# Desafio Azure Functions

Este projeto contém duas funções Azure Functions em Python, conforme os requisitos do desafio.

## Estrutura do Projeto

- **Function1 (Time Trigger)**: Coleta dados de uma URL específica e os salva em um container do Blob Storage.
- **Function2 (HTTP Request)**: Recebe um valor de taxa em formato JSON e salva um arquivo XML no Blob Storage.

## Funcionalidades

### 1. Função do Tipo Time Trigger

- **Descrição**: Esta função é executada automaticamente entre 18:40 e 19:30 em dias de semana.
- **URL de Coleta**: `https://sistemaswebb3-balcao.b3.com.br/featuresDIProxy/DICall/GetRateDI/eyJsYW5ndWFnZSI6InB0LWJyIn0=`
- **Armazenamento**: O JSON coletado é salvo em um container específico no Blob Storage.

#### Arquitetura

- A função verifica a data do JSON retornado e evita coletar dados novamente se já tiver coletado para a data atual.

### 2. Função do Tipo HTTP Request

- **Descrição**: Recebe uma requisição com o conteúdo `{"rate":"10,65"}`.
- **Formato de Saída**: Salva um arquivo XML no formato `<xml><rate value="10.65"></xml>` em um container no Blob Storage.

#### Arquitetura

- Utiliza uma fila para gerenciar requisições que possam resultar em timeout. Mesmo se a função exceder o tempo limite, o processamento será retomado a partir da fila.

## Como Testar

1. **Função Time Trigger**:

   - Certifique-se de que a função está agendada corretamente no Azure.
   - Verifique o Blob Storage para confirmar que os dados estão sendo salvos no horário programado.
2. **Função HTTP Request**:

   - Você pode testar a função utilizando ferramentas como Postman ou CURL.
   - Envie um POST request com o corpo JSON `{"rate":"10,65"}` para a URL da função.

## URL do Aplicativo

- Acesse o aplicativo em: [https://desafioazure2.azurewebsites.net](https://desafioazure2.azurewebsites.net)

## Considerações Finais

Este projeto foi desenvolvido para demonstrar o uso de Azure Functions com Python e a interação com Blob Storage. Para mais informações sobre Azure Functions, consulte a [documentação oficial da Microsoft](https://docs.microsoft.com/azure/azure-functions/).

## Contato

Para qualquer dúvida ou sugestão, entre em contato.
