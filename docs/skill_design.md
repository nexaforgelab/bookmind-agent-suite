# Skill è®¾è®¡è§è

BookMind çææ Skill å¿é¡»éµå¾ªæ¬è§èã

## 1. ç®å½ç»æ

```
skills/<skill-name>/
âââ SKILL.md            # å¿é
âââ scripts/            # è³å°ä¸ä¸ª entry script
â   âââ run_<skill>.py
âââ templates/          # å¯éï¼Jinja2 æ¨¡æ¿
âââ references/         # å¯éï¼ç¥è¯åº / ææ¡£
âââ tests/              # å¯éï¼ååæµè¯
```

## 2. SKILL.md å¿å¤å­æ®µ

```yaml
---
name: <skill-name>
description: ä¸å¥è¯è¯´æ + éç¨åºæ¯
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [...]
    category: ...
    requires_toolsets: [...]
---
```

æ­£æé¨åå¿é¡»åå«ï¼
- **When to Use**
- **Procedure**ï¼æ­¥éª¤ï¼
- **Safety and Copyright**
- **Verification**ï¼éªè¯æ åï¼
- **Example**ï¼å½ä»¤ç¤ºä¾ï¼
- **Failure Handling**

## 3. å¥å£èæ¬

`scripts/run_<skill>.py` å¿é¡»ï¼

1. è§£æåæ°ã
2. è°ç¨ `bookmind.skills_runtime.skill_executor.execute_skill` æå­æ¨¡åã
3. æç»æä»¥ JSON æå°å° stdoutã
4. ä¸ææªæè·å¼å¸¸ã

## 4. å¼å®¹æ§

- Skill å¿é¡»è½å¨ OpenClaw ä¸ Hermes ä¸­ä»¥ç¸åå¥å£è¿è¡ã
- ä»»ä½ Hermes ä¸å±è½åå¿é¡»éè¿ `metadata.hermes` æ¾å¼å£°æã

## 5. å®å¨

- ä»»ä½æä»¶åå¥åªè½è¿å¥ï¼
  - `BOOKMIND_OUTPUT_DIR`
  - `BOOKMIND_CACHE_DIR`
  - ç¨æ·æç¡®æå®ç®å½
- ä»»ä½å¤é¨å½ä»¤å¿é¡»èµ° `CommandAllowlist`ã
- ä»»ä½ç­å¼ç¨å¿é¡»å¯è¿½æº¯å°é¡µç  / ç« èã

## 6. çæ¬

`SKILL.md` ç `version` å­æ®µéµå¾ª semverã
ä»»ä½ç ´åæ§æ¹å¨å¿é¡»å majorã
