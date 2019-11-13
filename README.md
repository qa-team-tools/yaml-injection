# yaml-injection

## usage
### in python
```python
import yaml
from yaml_injection import InjectionLoader

with open(file_path) as in_:
    data = yaml.load(in_, InjectionLoader)

```

### in yaml

The key word is `inject`.

```yaml
inject: 
    file: path to file in local file system # or
    url: public url with yaml file # or
    ref: section subsection 
```

`ref` is a keys leading to section separated by space.

\* Yep it will works only if keys does not contain spaces.


## examples
Examples are gotten from tests. 

### example 1
`sub.yaml` 
```yaml
sub_only: sub_only
both_files: both_files_value_from_sub
non_map_object:
  - sub
non_map_only_sub:
  - sub_only
both_files_map:
  sub_only: sub_only
  both_files: both_files_value_from_sub
deep:
  deep:
    deep:
      map:
        sub_only: sub_only
        both_files: both_files_value_from_sub

```

`main.yml`

```yaml
inject:
  file: sub.yml

main_only: main_only
both_files: both_files_value_from_main
both_files_map:
  both_files: both_files_value_from_main
  main_only: main_only_value_from_main
deep:
  deep:
    deep:
      map:
        main_only: main_only
        both_files: both_files_value_from_main
non_map_object:
  - main
non_map_only_main:
  - main_only


```

will be loaded as:
```yaml
both_files: both_files_value_from_main
both_files_map:
  both_files: both_files_value_from_main
  main_only: main_only_value_from_main
  sub_only: sub_only
main_only: main_only
sub_only: sub_only
deep:
  deep:
    deep:
      map:
        main_only: main_only
        both_files: both_files_value_from_main
        sub_only: sub_only
non_map_object:
  - main
non_map_only_main:
  - main_only
non_map_only_sub:
  - sub_only
```


### example 2

```yaml
sections:
  sub:
    common:
      variables:
        job_name: sub_name
        script: sub

    job_1:
      only:
        - refs
      script:
        - make build
        - make start

    job_2:
      except:
        - tags
      script:
        - make build
        - make start

main:
  inject:
    ref: sections sub

  common:
    variables:
      script: main
      runner: main_runner

  job_1:
    only:
      - release

  job_2:
    before_script:
      - make prepare
```

will be loaded as:
```yaml
main:
  common:
    variables:
      job_name: sub_name
      runner: main_runner
      script: main
  job_1:
    only:
    - release
    script:
    - make build
    - make start
  job_2:
    before_script:
    - make prepare
    except:
    - tags
    script:
    - make build
    - make start
sections:
  sub:
    common:
      variables:
        job_name: sub_name
        script: sub
    job_1:
      only:
      - refs
      script:
      - make build
      - make start
    job_2:
      except:
      - tags
      script:
      - make build
      - make start
```