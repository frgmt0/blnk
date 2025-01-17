class TokenTracker:
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.session_messages = []
        
    def add_message(self, input_tokens, output_tokens, cache_created=0, cache_read=0, cache_hit_rate=0):
        """Add a message's token counts to the tracker"""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        
        # Calculate cumulative cache stats
        total_cached = sum(m.get('cache_read', 0) for m in self.session_messages)
        total_tokens = sum(m.get('input_tokens', 0) for m in self.session_messages)
        cumulative_hit_rate = (total_cached / total_tokens * 100) if total_tokens > 0 else 0
        
        self.session_messages.append({
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cache_created": cache_created,
            "cache_read": cache_read,
            "cache_hit_rate": cache_hit_rate,
            "cumulative_hit_rate": cumulative_hit_rate
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
        
        msg = f"\n📊 Token Usage Stats:\n"
        msg += f"Last Message: {last['input_tokens']} in / {last['output_tokens']} out"
        
        # Add cache performance details
        if last["cache_created"]:
            msg += f"\n🔄 Cached {last['cache_created']} new tokens"
        if last["cache_read"]:
            msg += f"\n📖 Retrieved {last['cache_read']} tokens from cache"
        if last.get("cache_hit_rate", 0) > 0:
            msg += f"\n✨ Cache Hit Rate: {last['cache_hit_rate']:.1f}%"
            
        # Add session totals
        msg += f"\n\n📈 Session Summary:"
        msg += f"\nTotal Tokens: {stats['total_tokens']}"
        msg += f" ({stats['total_input']} in / {stats['total_output']} out)"
        
        # Add cumulative cache performance
        if last.get("cumulative_hit_rate", 0) > 0:
            msg += f"\nOverall Cache Hit Rate: {last['cumulative_hit_rate']:.1f}%"
        
        return msg
