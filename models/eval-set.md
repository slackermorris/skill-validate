# JSON Schemas

Influence taken from [Anthropics Skill Creator](https://github.com/anthropics/skills/blob/b0cbd3df1533b396d281a6886d5132f623393a9c/skills/skill-creator/references/schemas.md?plain=1#L4).

---

## evals.json

Defines the evals for a skill. Located at `evals/evals.json` within the skill directory.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's example prompt",
      "files": ["evals/files/sample1.pdf"],
      "expectations": ["The output includes X", "The skill used script Y"]
    }
  ]
}
```

**Fields:**

- `skill_name`: Name matching the skill's frontmatter.
- `evals[].id`: Unique integer identifier.
- `evals[].prompt`: The task to execute.
- `evals[].files?`: Optional. A list of input file paths (relative to skill root).
- `evals[].expectations?`: Optional. List of verifiable statements

---

---

## [TIMESTAMP]-results.json

Captures the results of running a set of evals for a skill. Located at `evals/results/[TIMESTAMP]-results.json` within the skill directory, where `TIMESTAMP` is the timestamp when the results were collected.

```json
{
  "skill_name": "example-skill",
  "timestamp": "1773342950488",
  "total_skill_used_pass_rate": 0.86,
  "total_average_expectations_pass_rate": 0.86,
  "evals": [
    {
      "id": 1,
      "prompt": "User's example prompt",
      "skill_used": true,
      "expectations_pass_rate": 0.2,
      "expectations": [
        {
          "text": "The skill used script Y",
          "passed": true,
          "evidence": "Y script featured in the agents work log"
        }
      ]
    }
  ]
}
```

**Fields:**

- `skill_name`: Name matching the skill's frontmatter.
- `timestamp`: TODO
- `total_skill_used_pass_rate`: The fraction of the evals where the specified skill was used.

- `evals[].id`: The unique identifier of the eval.
- `evals[].prompt`: The task to execute.
- `evals[].skill_used`: Whether the skill was used in response to the prompt.

Below are fields related to more advanced testing of the skill. Being advanced, they are all optional.

- `total_average_expectations_pass_rate?`: Optional. The average of the evals expectation pass rate.

- `evals[].expectations_pass_rate?`: Optional. The ratio of expectations that were verified.
- `evals[].expectations?`: Optional. The list of expectations used to evaluate the skill.
- `evals[].expectations[].text?`: Optional. The skill behaviour to be verified.
- `evals[].expectations[].passed?`: Optional. Whether the skill behaviour was verified.
- `evals[].expectations[].evidence?`: Optional. Any evidence in support of the skill behaviour being verified or not.

---
