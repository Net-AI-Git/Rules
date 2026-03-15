## 1. Source and Scope

* **Reference:** [A successful Git branching model (nvie.com)](https://nvie.com/posts/a-successful-git-branching-model/).
* **When to use:** This model fits versioned releases and supporting multiple versions in the wild. For continuous delivery without versioning, simpler workflows may be preferred (per nvie 2020 reflection).
* **Mandate:** The project uses **GitFlow** as the **only** branching model. All branch creation, push targets, and merge targets follow this rule.

## 2. Main Branches (Infinite Lifetime)

* **`master` (or `main`):**
    * Source code at `HEAD` **always** reflects a **production-ready** state.
    * Every commit on `master` is a released version by definition.
    * Version tags (e.g. `v1.2.0`) are created **on `master`** after merging from a release or hotfix branch.
    * No direct pushes; updates only via merge from release or hotfix branches.

* **`develop`:**
    * Integration branch; source code at `HEAD` reflects the **latest delivered changes for the next release**.
    * Nightly or integration builds may be built from `develop`.
    * Feature branches merge **into** `develop`; release branches are created **from** `develop`.
    * No direct pushes; updates only via merge from feature, release, or hotfix branches.

## 3. Supporting Branches (Limited Lifetime)

Supporting branches are created when needed and **deleted** after merge. They are not special technically—only by how we use them.

### 3.1 Feature Branches

* **Branch off from:** `develop`
* **Merge back into:** `develop`
* **Naming:** Any name **except** `master`, `main`, `develop`, `release-*`, `hotfix-*`. Prefer prefixes such as `feature/<description>`, `fix/<description>`, `refactor/<description>`, `docs/<description>` (e.g. `feature/user-authentication`, `fix/memory-leak`).
* **Purpose:** Develop new features or non-urgent fixes for the upcoming or a future release. When finished, merge into `develop` (use `--no-ff` to preserve feature grouping in history). Then delete the feature branch.

### 3.2 Release Branches

* **Branch off from:** `develop`
* **Merge back into:** `master` **and** `develop`
* **Naming:** `release-*` (e.g. `release-1.2`, `release-2.0`).
* **Purpose:** Prepare a new production release. Only minor bug fixes, version bumps, and metadata (CHANGELOG, build dates) on this branch. No large new features. When ready: merge into `master` and tag the version on `master`; merge into `develop`; delete the release branch.

### 3.3 Hotfix Branches

* **Branch off from:** `master`
* **Merge back into:** `master` **and** `develop` (or into the current release branch if one exists—see below).
* **Naming:** `hotfix-*` (e.g. `hotfix-1.2.1`).
* **Purpose:** Fix a critical bug in production immediately. Create from the tag on `master` that marks the production version. Bump version (e.g. PATCH). When finished: merge into `master` and tag; merge into `develop` (or into the active release branch); delete the hotfix branch.

* **Exception (nvie):** If a **release branch** currently exists, merge the hotfix into that **release branch** instead of `develop`, so the fix is included in the upcoming release. If the fix is also needed in `develop` immediately, merge into `develop` as well.

## 4. Agent Decision Table: Which Branch and Where to Push/Merge

Use this table to decide which branch to create and where to merge. **Never push directly to `master` or `develop`**; all updates go via merge from a supporting branch.

| Situation | Create branch | From | Push commits to | When ready, merge to | Then |
|-----------|---------------|------|-----------------|----------------------|------|
| Starting a new feature | `feature/<description>` | `develop` | The feature branch | `develop` (MR/PR) | Delete feature branch |
| Non-urgent bug fix (not production) | `feature/<description>` or `fix/<description>` | `develop` | That branch | `develop` (MR/PR) | Delete branch |
| Preparing release for version x.y | `release-x.y` | `develop` | The release branch | `master` then `develop` | Tag on `master` (e.g. `vx.y`); delete release branch |
| Urgent production fix | `hotfix-x.y.z` | `master` | The hotfix branch | `master` then `develop` (or release branch if exists) | Tag on `master`; delete hotfix branch |

* **Creating a feature branch:** `git checkout develop` then `git checkout -b feature/<name> develop`. Push commits to `feature/<name>`. Open MR/PR **into `develop`**. After merge, delete the feature branch.
* **Creating a release branch:** When `develop` is ready for release, e.g. `git checkout -b release-1.2 develop`. Do version bump and CHANGELOG on this branch. When ready: merge to `master`, tag on `master`, merge to `develop`, delete `release-1.2`.
* **Creating a hotfix branch:** From `master`, e.g. `git checkout -b hotfix-1.2.1 master`. Fix and bump version. Merge to `master`, tag on `master`, merge to `develop` (or to current release branch if one exists). Delete hotfix branch.

## 5. Merge and Tag Rules

* **Feature → develop:** Merge with `--no-ff` when possible so the feature appears as a single merge commit in history.
* **Release → master:** Merge release branch into `master`. Create annotated tag on `master` (e.g. `git tag -a 1.2 -m "Release 1.2"`). Then merge the same release branch into `develop`.
* **Hotfix → master:** Merge hotfix into `master`, tag on `master`, then merge hotfix into `develop` (or into the active release branch first, then that release will bring the fix into `develop` when finished).

## 6. References

* **Version numbering, changelog, and release metadata:** **See** rule: versioning-and-release-management (in .amazonq/rules) for semantic versioning, CHANGELOG format, and release preparation steps (version bump, CHANGELOG, tests) that are performed **on the release branch** before merging to `master`.
* **Code review and branch protection:** **See** rule: code-review-and-collaboration (in .amazonq/rules) for PR/MR requirements and protection of `master` and `develop`.
