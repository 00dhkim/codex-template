# Codex Template

새 프로젝트를 시작할 때 복사하거나 GitHub template repository로 사용하기 위한 Codex 기본 템플릿이다.

## 포함 내용

- `AGENTS.md`
  새 프로젝트 루트에 둘 Codex 작업 지침
- `.codex/skills/project-full-access/`
  현재 프로젝트의 `.codex/config.toml`에 full-access 기본값을 넣는 스킬

## 권장 사용 방법

1. 이 폴더를 GitHub 레포로 올린다.
2. 새 프로젝트를 만들 때 이 레포를 template으로 사용하거나, 필요한 파일만 복사한다.
3. 새 프로젝트 루트에 `AGENTS.md`가 유지되는지 확인한다.
4. `project-full-access` 스킬을 명시적으로 쓰려면, 필요 시 이 레포의 `.codex/skills/project-full-access`를 `~/.codex/skills/project-full-access`로 복사해 전역 스킬로 등록한다.

## 빠른 시작

```bash
cp AGENTS.md /path/to/new-project/AGENTS.md
mkdir -p ~/.codex/skills
cp -R .codex/skills/project-full-access ~/.codex/skills/
```

그다음 새 프로젝트 디렉터리에서 Codex를 열고 필요하면 `$project-full-access`를 호출한다.
