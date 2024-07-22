import simple_fast_regex as sfr
import time

# Rust Implementation
engine = sfr.RegexEngine()

# Create one pattern that needs to escaping and one that doesn't
escape_pattern = "function addAllow(address holder, bool allowApprove) external onlyOwner { allow[holder] = allowApprove;"
no_escape_pattern = "if \\(owner == address\\(\\w+\\)\\) \\{ _allowances\\[owner\\]\\[spender\\] = amount; emit Approval\\(owner, spender, amount\\); \\} else \\{ _allowances\\[owner\\]\\[spender\\] = 0;"

# Add the patterns to the engine
engine.add_patterns(patterns=[escape_pattern], escape=True)
engine.add_patterns(patterns=[no_escape_pattern], escape=False)

# Run the search
TEXT0 = "No string should be found for this case"
TEXT1 = """function addAllow(address holder, bool allowApprove) external onlyOwner { allow[holder] = allowApprove;"""
TEXT2 = """if (owner == address(0xasida9sdu9asd)) { _allowances[owner][spender] = amount; emit Approval(owner, spender, amount); } else { _allowances[owner][spender] = 0;"""

matches = engine.search(TEXT0) # 0 matches
print(matches)

matches = engine.search(TEXT1) # 1 match
print(matches)

matches = engine.search(TEXT2) # 1 match
print(matches)

all_texts_together = TEXT0 + " \n " + TEXT1 + " \n " + TEXT2
matches = engine.search(all_texts_together) # 2 matches
print(matches)

# Print the raw_patterns list to make sure it's working fine
print(engine.raw_patterns)
