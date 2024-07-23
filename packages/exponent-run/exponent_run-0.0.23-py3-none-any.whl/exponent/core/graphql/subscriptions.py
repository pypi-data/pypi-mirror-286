AUTHENTICATED_USER_SUBSCRIPTION = """
    subscription {
            testAuthenticatedUser {
                __typename
                ... on UnauthenticatedError {
                    message
                }
                ...on Error {
                    message
                }
                ... on User {
                    userUuid
                }
            }
        }
"""

CHAT_EVENTS_SUBSCRIPTION = """
  subscription ChatEvents(
    $prompt: Prompt
    $codeBlockConfirmation: CodeBlockConfirmationResponse
    $fileWriteConfirmation: FileWriteConfirmationResponse
    $chatUuid: String!
    $parentUuid: String
    $model: LiteLLMModels!
    $useToolsConfig: UseToolsMode!
    $requireConfirmation: Boolean
    $strategyNameOverride: StrategyName
  ) {
    authenticatedChat(
      chatInput: {
        prompt: $prompt
        codeBlockConfirmation: $codeBlockConfirmation
        fileWriteConfirmation: $fileWriteConfirmation
      }
      parentUuid: $parentUuid
      chatConfig: {
        chatUuid: $chatUuid
        model: $model
        useToolsConfig: $useToolsConfig
        requireConfirmation: $requireConfirmation
        strategyNameOverride: $strategyNameOverride
      }
    ) {
      __typename
      ... on UnauthenticatedError {
        __typename
        message
      }
      ... on MessageChunkEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        role
        content
      }
      ... on MessageEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        role
        content
        attachments {
          ... on FileAttachment {
            file {
              filePath
              workingDirectory
            }
            content
          }
          ... on URLAttachment {
            url
            content
          }
        }
      }
      ... on CodeBlockChunkEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        language
        content
      }
      ... on CodeBlockEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        language
        content
        requireConfirmation
      }
      ... on CodeBlockConfirmationEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        codeBlockUuid
        accepted
      }
      ... on CodeExecutionEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        codeBlockUuid
        content
      }
      ... on CodeExecutionStartEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        codeBlockUuid
      }
      ... on FileWriteChunkEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        filePath
        language
        writeStrategy
        content
      }
      ... on FileWriteEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        filePath
        language
        writeStrategy
        content
        requireConfirmation
      }
      ... on FileWriteConfirmationEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        fileWriteUuid
        accepted
      }
      ... on FileWriteResultEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        fileWriteUuid
        content
      }
      ... on FileWriteStartEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
        fileWriteUuid
      }
      ... on RemoteStartEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
      }
      ... on RemoteEndEvent {
        __typename
        chatUuid
        eventUuid
        parentUuid
      }
    }
  }
"""
