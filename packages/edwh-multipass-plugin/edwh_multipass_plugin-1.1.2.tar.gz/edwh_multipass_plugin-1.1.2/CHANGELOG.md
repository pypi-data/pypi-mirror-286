# Changelog

<!--next-version-placeholder-->

## v1.1.2 (2024-07-22)

### Fix

* Indentation error ([`bfda2d7`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/bfda2d76fb7adfda377b1919225131419b5f3114))

## v1.1.1 (2024-07-12)

### Fix

* Slightly improved readable formatting for `ew mp.mounts` ([`5fc1a35`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/5fc1a35cb50d4ed6448790d1421dcfc8d1a15614))

### Documentation

* Manually fix changelog ([`f64ec4c`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/f64ec4c801b6df5e1708fe5e177cb7bdfe8b9c41))

## v1.1.0 (2024-07-12)

### Feature

* Allow edwh to manage mp mounts, so we can do `remount` if mp loses the mounts ([`8b5c5ae`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/8b5c5aee3d5b520de5b4a76f6ded207782cc68ba))
* Add `ew mp.mount` which stores mounts in order to do `ew mp.remount` later on ([`a208679`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/a208679af06b411d81510c47c09ba81edce6feb3))

### Fix

* Improve typing (mypy) ([`5554a42`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/5554a42ca9902921c254a4e20c5a909dce049bbb))
* Improved remote execution (worked only locally before) - requires edwh>=0.43 ([`0eab701`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/0eab701b70a83c7d4e30a9d5cf61ff11349985fd))


## v1.0.3 (2024-07-04)

### Fix

* Update way too long command suggestion at the end of `prepare-multipass` to simply remote.prepare-generic-server (since that's probably your next step) ([`da20a6e`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/da20a6e6d465c14b1f0d6ba389c649f79f39fd81))
* Minor improvements in typing, docs, refactoring ([`b64056b`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/b64056bffdbf6b9e0dd77ae3f0eb7bcad9700a9d))

## v1.0.2 (2024-04-12)

### Fix

* Use require_sudo for improved password prompting + general refactoring ([`b2fd319`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/b2fd3192097800832254fab9cd691c20acd29f66))

## v1.0.1 (2023-05-01)

