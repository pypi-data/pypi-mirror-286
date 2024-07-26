HALT_CHAT_STREAM_MUTATION: str = """
  mutation HaltChatStream($chatUuid: String!) {
    haltChatStream(chatUuid: $chatUuid) {
      __typename
    }
  }
"""
