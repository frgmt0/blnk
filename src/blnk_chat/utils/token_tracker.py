class TokenTracker:
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.session_messages = []
        
    def add_message(self, input_tokens, output_tokens, cache_created=0, cache_read=0):
        """Add a message's token counts to the tracker"""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        
        self.session_messages.append({
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cache_created": cache_created,
            "cache_read": cache_read
        })
        
    def get_stats(self):
        """Get current token statistics"""
        return {
            "total_input": self.total_input_tokens,
            "total_output": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "messages": len(self.session_messages),
            "last_message": self.session_messages[-1] if self.session_messages else None
        }
        
    def format_stats(self):
        """Format token statistics for display"""
        stats = self.get_stats()
        last = stats["last_message"]
        
        msg = f"\nToken Usage:\n"
        msg += f"Last Message: {last['input_tokens']} in / {last['output_tokens']} out"
        
        if last["cache_created"]:
            msg += f" (Cached {last['cache_created']} tokens)"
        elif last["cache_read"]:
            msg += f" (Read {last['cache_read']} from cache)"
            
        msg += f"\nSession Total: {stats['total_tokens']} tokens"
        msg += f" ({stats['total_input']} in / {stats['total_output']} out)"
        
        return msg
