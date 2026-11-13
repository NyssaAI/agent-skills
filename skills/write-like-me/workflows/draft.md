# Workflow: Draft in User Voice

> [!IMPORTANT] Scope Directive
> This workflow handles drafting, rewriting, and replying in the user's authentic writing voice using resolved `Writing Voice Profile` bundles. It does NOT own modifying, calibrating, or creating `Writing Voice Profile` bundles (owned by `maintain.md`), filing drafted notes into `vault_root` (owned by `para-vault`), or capturing/checking in on structured tasks and daily plans (owned by `daily-tasks`).

Produce the requested text using applicable, supported voice guidance.

1. Identify the audience, purpose, supplied facts, and required format from the task. Apply personal voice to material written on the user's behalf; preserve attribution and wording where quoted material, `Source Record` exports, third-party text, or destination requirements constrain the task.
2. Resolve one complete explicit, `repo_root`, or `user_home` `Writing Voice Profile` bundle using [shared storage](../references/storage.md). Read `VOICE.md`, optional `STYLE.md`, and relevant approved examples only from that selected bundle; interpret them with the [profile schema](../references/profile-schema.md). Do not borrow another `repo_root`'s profile or create a profile during drafting.
3. Follow explicit task directions and required destination standards, then the appropriate context mode and approved preferences. Draft without changing facts, commitments, intent, or uncertainty. Use [drafting and review](../references/drafting-and-review.md) to compare style and meaning separately.
4. Present useful finished text in the requested form. If no profile exists, briefly state that limitation and offer [voice setup](maintain.md) while still completing the draft from available task instructions and supplied examples. Do not claim an evidence-backed voice match when evidence is absent or sparse.

Ordinary drafting reads profile files and leaves their bytes unchanged. Route explicit requests to learn or save preferences to [maintain voice profile](maintain.md); acceptance of this draft alone does not authorize profile updates, example retention, or sending/publishing the text.

---

## Verification

Before reporting completion of any personal-voice drafting task:
- [ ] Confirm all supplied facts, commitments, dates, constraints, quoted material, and uncertainty levels match the source request without fabrication or drift.
- [ ] Confirm voice guidance was resolved atomically from one precedence-selected `Writing Voice Profile` bundle (`explicit pointer` $\rightarrow$ `repo_root` $\rightarrow$ `user_home`) without cross-scope merging or probing retired `.nyssaai`/`.nyssa` paths.
- [ ] Confirm all `VOICE.md`, `STYLE.md`, and curated example files remain completely unmodified (read-only during drafting).
- [ ] If no `Writing Voice Profile` bundle was present, confirm the limitation was disclosed honestly without claiming an evidence-backed match.
