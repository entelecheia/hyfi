<!--next-version-placeholder-->

## v1.12.1 (2023-07-28)

### Fix

* **generator:** Skip VAR_KEYWORD params in GENERATOR ([`34cc59a`](https://github.com/entelecheia/hyfi/commit/34cc59a7addf8b157dd861b5f27cbd947ea3377e))
* **pipe:** Add kwargs support to save_dataset_to_disk function ([`a226554`](https://github.com/entelecheia/hyfi/commit/a22655491a38618a1d4b6b4bfb5285cf49f33bac))

## v1.12.0 (2023-07-28)

### Feature

* **generator:** Add pipe config support for HyFI ([`1696ee9`](https://github.com/entelecheia/hyfi/commit/1696ee9bf659a5e6d75cde42b8f163f2e29d38e8))
* **tests:** Add new test_base.py for hyfi composer ([`9887ee1`](https://github.com/entelecheia/hyfi/commit/9887ee1eca9d92bb689d1e015361f874fb4f1391))
* **composer/base:** Add save_hyfi_config method and TestModel class to base module ([`9fbbd3c`](https://github.com/entelecheia/hyfi/commit/9fbbd3c321c523e71879300d0dc66d22f66e2850))
* **tests:** Add test for generating configs in Hyfi composer ([`a1fdce4`](https://github.com/entelecheia/hyfi/commit/a1fdce4eb7714d25ad9a0d22a6589b34997e44ae))
* **hyfi:** Add GENERATOR to HyFi class ([`4f93600`](https://github.com/entelecheia/hyfi/commit/4f9360040248d575d923e4688e8c32007a84745a))
* **core:** Add config_root property to GlobalHyFIConfig class ([`fc16744`](https://github.com/entelecheia/hyfi/commit/fc16744cf5127936b938f09fed6080c33bb3d3cc))
* **utils:** Add new utilities including object identification and module name checks ([`e962ae1`](https://github.com/entelecheia/hyfi/commit/e962ae1240d84b4a39a77e98f9ecfd4c464c0b6c))
* **hyfi-composer:** Add generator module ([`5d4e2ee`](https://github.com/entelecheia/hyfi/commit/5d4e2ee58797a8852d411e0b9ed2ef9288340125))
* **composer:** Add generator to imports and __all__ list ([`cab15ec`](https://github.com/entelecheia/hyfi/commit/cab15ecc362acdad2c52a621a7d8773212c274af))

### Fix

* **hyfi/conf/pipe:** Add pipe_obj_arg_name in dataset configuration files ([`449b596`](https://github.com/entelecheia/hyfi/commit/449b596a8e006d27ce631bec27934667181c77da))
* **hyfi:** Add user_config_path and config_dirname parameters, modify way to append config-dir in sys ([`dda715e`](https://github.com/entelecheia/hyfi/commit/dda715ed21476b491f434eddf5eaf93951c06137))
* **core:** Add user_config_path and config_dirname options ([`94aba6c`](https://github.com/entelecheia/hyfi/commit/94aba6c7ebae96c832f457852f0183291ea9fb31))
* **hydra:** Use plugin name in search path ([`58dd768`](https://github.com/entelecheia/hyfi/commit/58dd768f0232c6f448bf27f8d1157a18259e7af9))
* **pipe:** Remove run_with from configuration ([`8643258`](https://github.com/entelecheia/hyfi/commit/8643258415affdc1408cba894161ac4ddbc98fe5))

## v1.11.0 (2023-07-26)

### Feature

* **hyfi:** Add load_dataset_from_disk, sample_dataset, and save_dataset_to_disk configurations ([`265db31`](https://github.com/entelecheia/hyfi/commit/265db31a06a4f0704f684e9959c21596bf55ce71))
* **hyfi/conf/run:** Add new __init__.yaml for run configuration ([`7a72b85`](https://github.com/entelecheia/hyfi/commit/7a72b85ef550d798c7dcb22f2d2e689b7cd5869f))
* **config:** Add load_dataframes, preprocessing_esg_ratings, and save_dataframes configurations ([`4a6ea2a`](https://github.com/entelecheia/hyfi/commit/4a6ea2a5f7a88e556fa6afc8c48cb87c41e4716c))
* **config:** Add new default run commands in config files ([`1199686`](https://github.com/entelecheia/hyfi/commit/11996863b10fa823ab97102300996d8d6566aa12))

### Fix

* **pipeline/configs:** Handle both string and dict inputs for run config ([`793f218`](https://github.com/entelecheia/hyfi/commit/793f2180977a7c75ccd675425a7162a660a29629))
* **pipe:** Replace run/kwargs with run_target/run_kwargs in general_instance_methods and dataframe_instance_methods ([`eff671c`](https://github.com/entelecheia/hyfi/commit/eff671cdd4c5ca25246303d8be001cc17018477f))
* **hyfi:** Simplify dataset yaml configurations ([`95f03f3`](https://github.com/entelecheia/hyfi/commit/95f03f3aeaa20619f10b34768893e32cf839f9bd))
* **composer:** Change 'run_with' to 'run' in key substitution ([`3ef33ba`](https://github.com/entelecheia/hyfi/commit/3ef33ba76ce6e6a2bec43c97a94a91f6a8854451))
* **pipeline:** Replace run with with in test_general.yaml ([`953070a`](https://github.com/entelecheia/hyfi/commit/953070a06cc4ba10aec892c77a88fb7369337e65))

## v1.10.3 (2023-07-26)

### Fix

* **pipe:** Add logging details to save_dataset_to_disk function ([`74b1661`](https://github.com/entelecheia/hyfi/commit/74b1661a54b6f75c8ed72f68999113dbf86c65ec))
* **config:** Correct typo in workflow_name attribute, correct typo in workflow log message ([`cf3e579`](https://github.com/entelecheia/hyfi/commit/cf3e5791d2288fdd385b3404bb1932eee63ec0a0))
* **hyfi:** Modify debug configurations and logging levels, introduce new config files for hydra and info modes ([`cf62132`](https://github.com/entelecheia/hyfi/commit/cf621328480bfde2b1583fa887fb409d64876742))

## v1.10.2 (2023-07-26)

### Fix

* **composer:** Use local variables for config_module and plugins ([`9ad01fd`](https://github.com/entelecheia/hyfi/commit/9ad01fd879716d85f11ece7e9de792761293503e))

## v1.10.1 (2023-07-26)

### Fix

* **dependencies:** Update datasets version range in pyproject.toml ([`b49c5b8`](https://github.com/entelecheia/hyfi/commit/b49c5b8c86c2f3a00475aa7819e57c9ea391cfc9))
* **pipeline:** Add elapsed time logging ([`a32a2c2`](https://github.com/entelecheia/hyfi/commit/a32a2c273f3da9eee890880582f50d9b4ae25714))
* **hyfi/pipe:** Add verbose logging options, import Dataset from arrow_dataset instead of datasets, add num_heads and num_tails parameters ([`6f8f8f8`](https://github.com/entelecheia/hyfi/commit/6f8f8f8cd066522df18136e0aba0560207b417b9))
* **hyfi:** Use global hyfi instead of hyfi config module path ([`9d8f663`](https://github.com/entelecheia/hyfi/commit/9d8f66340c4d1d75902a59328ac2e51485f8bf2b))
* **core:** Updated HyfiConfig class to use __global_hyfi__ more extensively ([`3833b05`](https://github.com/entelecheia/hyfi/commit/3833b055fe9de42fb6340375de78fb7fe8c0613f))
* **core:** Enhance type annotations and properties definition ([`ea26dee`](https://github.com/entelecheia/hyfi/commit/ea26dee61bd19447767423276f839d748a16f94e))
* **composer:** Replace global constant paths with attributes from __global_hyfi__ ([`8f3e8c2`](https://github.com/entelecheia/hyfi/commit/8f3e8c2786341e8f4a804e178c00f9bb7254cffb))
* **hyfi:** Change __hyfi_path__ to __global_hyfi__ in src_path default ([`86e1aaa`](https://github.com/entelecheia/hyfi/commit/86e1aaa8b96fecf9e7cb1f6e11199058b4f2c65d))
* **hyfi:** Use global hyfi for package name and version base ([`1acd9ca`](https://github.com/entelecheia/hyfi/commit/1acd9cac95b31740dd1ed727016ed84b526ae139))
* **utils:** Improve get_caller_module_name in packages.py ([`4b5494d`](https://github.com/entelecheia/hyfi/commit/4b5494d4720fc692548edb7d85c48e97b12a8d2f))

## v1.10.0 (2023-07-25)

### Feature

* **hyfi/main:** Add config_module and user_config path resolvers ([`2e14fb4`](https://github.com/entelecheia/hyfi/commit/2e14fb4c655cd0cc792ff6b50ce8299261925005))
* **core:** Add type hinting to hyfi_path and home_path functions, add user_config_path and config_module_path functions ([`0dd36da`](https://github.com/entelecheia/hyfi/commit/0dd36dab6d4b63739eaa46458b03f311e6dfbc4b))
* **hyfi:** Add project root and workspace path resolvers ([`3dff304`](https://github.com/entelecheia/hyfi/commit/3dff3041824f04881d8bb38058074a41a03fc028))
* **hyfi/core:** Add project root and workspace path properties ([`d59dcb6`](https://github.com/entelecheia/hyfi/commit/d59dcb66ba6d338e03885edabcb4e69af7c7b312))

### Documentation

* Add new sections to pipe.md ([`78a5ff6`](https://github.com/entelecheia/hyfi/commit/78a5ff6acb6fabff5f9bf7863fb040c4a30c27b0))

## v1.9.4 (2023-07-25)

### Fix

* **core:** Change object property access ([`dba1f0d`](https://github.com/entelecheia/hyfi/commit/dba1f0d520be457a4df83bbc05ed4e9d1ce1427e))

## v1.9.3 (2023-07-24)

### Fix

* **HyFi:** Change 'package_name' parameter to 'package_path' ([`4edd36b`](https://github.com/entelecheia/hyfi/commit/4edd36b6ba32db319b356ac974f5c1dc5f2be0ac))
* **core:** Replace 'config_path' with 'config_dirname', add properties, modify 'GlobalHyFIConfig' class ([`e6a3921`](https://github.com/entelecheia/hyfi/commit/e6a3921576324f9054d2ea088955e7df5bc4a2e1))
* **hyfi:** Change package_name parameter to package_path in initialize_global_hyfi function ([`9c594a6`](https://github.com/entelecheia/hyfi/commit/9c594a6b570a7044c9bce000b2c108c72f5ea6ed))
* **hyfi:** Replace __package_name__ with package_name ([`55f14e1`](https://github.com/entelecheia/hyfi/commit/55f14e1a8024be16bcd535c1affe83e6375ed303))
* **hyfi:** Add plugins parameter to initialize_global_hyfi function ([`0a3affd`](https://github.com/entelecheia/hyfi/commit/0a3affdf917d5b2889ebf197e5649507fa146f5f))

## v1.9.2 (2023-07-24)

### Fix

* **hyfi:** Fix plugin loading functionality ([`eb5d14f`](https://github.com/entelecheia/hyfi/commit/eb5d14fa905fe35f076f65cd66f725ede5b96e82))
* **hydra:** Comment out caller_config_module related code ([`4048e86`](https://github.com/entelecheia/hyfi/commit/4048e8655e308309016fa24add5c668d8fe8a974))
* **core:** Improve docstrings and remove import check in get_plugins ([`24bded7`](https://github.com/entelecheia/hyfi/commit/24bded7af64ff0d44e725213c3fbf8a26f819f0a))
* **hyfi:** Add plugin initialization details ([`dfc238a`](https://github.com/entelecheia/hyfi/commit/dfc238ab8d1ebd77be61129409d8ca392168ade8))

## v1.9.1 (2023-07-24)

### Fix

* **core:** Change the way plugins are loaded ([`9a41ab7`](https://github.com/entelecheia/hyfi/commit/9a41ab7d94fc556bdd886b8e918a0dfb9ee2e194))
* **utils:** Add is_importable method to PKGs class ([`65fbc33`](https://github.com/entelecheia/hyfi/commit/65fbc339b7b627b9d0d03370a5ad1640088758ec))
* **hyfi:** Add plugins parameter to initialize_global_hyfi function ([`4ce5cf7`](https://github.com/entelecheia/hyfi/commit/4ce5cf7430f870213573ecf227052bba70380cae))
* **utils/packages:** Add exception handling to get_caller_module_name function ([`75ddcef`](https://github.com/entelecheia/hyfi/commit/75ddcef7601ddf850d68769677e29cf116f8320f))

## v1.9.0 (2023-07-24)

### Feature

* **tests/hyfi:** Add plugins parameter to initialize function ([`97b0252`](https://github.com/entelecheia/hyfi/commit/97b0252385ec1593c910e01dd77d702c08b6a590))
* **hydra-main:** Add plugins parameter ([`2b708ac`](https://github.com/entelecheia/hyfi/commit/2b708ac13602103ad630583dc3f99f4fcd6a9b9b))
* **hydra:** Add support for plugins in initialize_config and create_config_search_path functions ([`1a4c833`](https://github.com/entelecheia/hyfi/commit/1a4c8336232103df4fd0f07876bb0f8ef14c4fc8))
* **core:** Add plugin loading functionality ([`f680547`](https://github.com/entelecheia/hyfi/commit/f680547eb3cdb677ec629cb9cd603592aeab76fb))
* **composer:** Add plugins support ([`61f04d4`](https://github.com/entelecheia/hyfi/commit/61f04d42c60b5deda31c8149c5a779b572eb8d62))
* **hyfi:** Add initialize_global_hyfi function ([`1fd61f6`](https://github.com/entelecheia/hyfi/commit/1fd61f6af6c677e6624e4017f407d76e1399e830))
* **hyfi:** Add plugins support in hyfi_main and hydra_main functions ([`61b62f6`](https://github.com/entelecheia/hyfi/commit/61b62f642e47d3db13922415332584d5dd5d9c08))

## v1.8.3 (2023-07-23)

### Fix

* **workflow:** Enhance tasks population in WorkflowConfig ([`6b1e43a`](https://github.com/entelecheia/hyfi/commit/6b1e43aeb5c001972d1453f5746d56bc1066d8c5))
* **pipeline:** Enhance logger information and pipeline handling ([`8951d7d`](https://github.com/entelecheia/hyfi/commit/8951d7d3c02da8971d59cc1cab880cf2c3669bc5))
* **task:** Change task_name to dynamic variable ([`f218cfc`](https://github.com/entelecheia/hyfi/commit/f218cfcc8381d678114eddc6dad147dca0db1cf8))

## v1.8.2 (2023-07-23)

### Fix

* **hyfi:** Add global_hyfi initialization method to HyFI ([`81c8f6f`](https://github.com/entelecheia/hyfi/commit/81c8f6f046e2c3e69d4e832a57c9ebb387ef0239))

## v1.8.1 (2023-07-22)

### Fix

* **hyfi/core/config:** Rename hyfi_config_path to hyfi_config_module_path ([`13b170e`](https://github.com/entelecheia/hyfi/commit/13b170ee94acb172d0cda96baf72581673223026))
* **core:** Rename config path methods ([`8cf724e`](https://github.com/entelecheia/hyfi/commit/8cf724e99495c2f8341d2088db4f7f775ff3a14d))
* **hyfi:** Change config_path to config_module_path ([`cb61b92`](https://github.com/entelecheia/hyfi/commit/cb61b92706a933b0954aeda8657b77f24781997b))
* **core:** Add __config_path__ field and modify config_module property ([`23fee24`](https://github.com/entelecheia/hyfi/commit/23fee24e08ef584ef09430e69ab6023cafaa3776))
* **core:** Add config_name attribute to GlobalHyFIConfig class ([`c653008`](https://github.com/entelecheia/hyfi/commit/c65300878d39912a29921eb2e3defaded39bebee))
* **hyfi:** Modify default parameter handling in hyfi_main and hydra_main functions ([`5a040a5`](https://github.com/entelecheia/hyfi/commit/5a040a5a6a0f6d8ea3ad6f8b52a487e1aac89482))

## v1.8.0 (2023-07-22)

### Feature

* **core:** Add initialize method to GlobalHyFIConfig ([`ab6474f`](https://github.com/entelecheia/hyfi/commit/ab6474f658b274cbda73f2d284e4d0c99d4cbbc2))
* **hyfi:** Add initialize_global_hyfi function ([`9b41404`](https://github.com/entelecheia/hyfi/commit/9b4140451a2942e59a5d0932b0fae06b193e7284))

### Fix

* **hyfi/main:** Correct the location of __hyfi_version__ import in __init__.py ([`bcf0c14`](https://github.com/entelecheia/hyfi/commit/bcf0c14ec81adbafa8b2595d257497f77a5fcc3d))
* **hyfi/core:** Replace __about__ with __global_hyfi__ and self.about ([`f2f6bf0`](https://github.com/entelecheia/hyfi/commit/f2f6bf0184bc29ba5ded7d0dde00d431f5fc9386))
* **core:** Update configuration structure and methods ([`06f1b42`](https://github.com/entelecheia/hyfi/commit/06f1b42fdfa33f7a38650737ffad8857d6251ab4))
* **hyfi:** Replace __hydra_config__ with __global_hyfi__ ([`17ffe6c`](https://github.com/entelecheia/hyfi/commit/17ffe6ca6b00f999b8175182de488c5a3d312401))
* **hyfi:** Replace about with global_hyfi in module imports ([`d9beab0`](https://github.com/entelecheia/hyfi/commit/d9beab0f9b6b02bb7e774e20fda5b90ee1a9f163))

## v1.7.1 (2023-07-22)

### Fix

* **hyfi:** Introduce package name and path handling. ([`8aaddeb`](https://github.com/entelecheia/hyfi/commit/8aaddeb63d40d4f9f8c96c16afdf42c04d69503d))
* **hyfi.core:** Change __config_module_path__ to __hyfi_config_module_path__ ([`bf25faa`](https://github.com/entelecheia/hyfi/commit/bf25faaa7b444f637868ca519833733f30693184))
* **hyfi/core/config:** Consolidate import statements and add package_name property ([`f8b7e04`](https://github.com/entelecheia/hyfi/commit/f8b7e047efc8379880a7a8648e772c5192c36d5d))
* **core:** Rename and add function in init file ([`4d865ac`](https://github.com/entelecheia/hyfi/commit/4d865ac0d22e8412af42b0f678925fc374cfd774))
* **hyfi/conf:** Update project_name variable in __init__.yaml ([`88d29a2`](https://github.com/entelecheia/hyfi/commit/88d29a24cb5db193ffd2ebbc2747d2fe2fb57aa1))
* **path:** Rename app to package in configuration ([`eeffda8`](https://github.com/entelecheia/hyfi/commit/eeffda88b4024fa5983dae6aa01256070df1ac1c))
* **hyfi:** Rename attribute names with hyfi prefix ([`d4f1d39`](https://github.com/entelecheia/hyfi/commit/d4f1d39b0db64082422b25882b23b8670cdf4248))
* **hyfi:** Change __package_name__ to __hyfi_package_name__ ([`a3921c3`](https://github.com/entelecheia/hyfi/commit/a3921c399abbbb655e08da742ea1841e61dcd455))

## v1.7.0 (2023-07-22)

### Feature

* **hyfi:** Add app path and version resolvers ([`2352c56`](https://github.com/entelecheia/hyfi/commit/2352c564add16c90001089141c3b34e23954b293))
* **hydra/main:** Add overrides parameter to main function ([`2288a25`](https://github.com/entelecheia/hyfi/commit/2288a2500100679aa272c1d5ca6820c9c0147044))
* **core:** Add app version and path functions ([`62b8388`](https://github.com/entelecheia/hyfi/commit/62b8388718b26c00f0cd4bc65c4edfb89f5ab215))
* **hyfi/conf/path:** Add app path in __init__.yaml ([`8b8e04a`](https://github.com/entelecheia/hyfi/commit/8b8e04a90a68443ed11c52bd329a866b1de55f1c))
* **hyfi/conf:** Add version to configuration ([`417c260`](https://github.com/entelecheia/hyfi/commit/417c2609b5af4a0a9a186c93556d388296cde71c))
* **hyfi/about:** Add package path and version to AboutConfig ([`483ba99`](https://github.com/entelecheia/hyfi/commit/483ba992cea502241761f4695f2a629d1cf3d38e))
* **hyfi:** Add overrides option in hyfi main functions ([`d0649ce`](https://github.com/entelecheia/hyfi/commit/d0649ce0c9b44e4738be58f206490ba26c305ee4))

### Fix

* **hyfi:** Delete version specification ([`f829bcb`](https://github.com/entelecheia/hyfi/commit/f829bcb81ed9f86a1e9a269958f8e5c2c4c8d073))

## v1.6.4 (2023-07-22)

### Fix

* **hyfi:** Change append_search_path order ([`4c18e01`](https://github.com/entelecheia/hyfi/commit/4c18e0158f44279a354a2c14ff62ef83245fe64e))

## v1.6.3 (2023-07-22)

### Fix

* **hydra/utils:** Simplify search_path creation ([`f4881a7`](https://github.com/entelecheia/hyfi/commit/f4881a7c678b314dca6feedc3ba026cca38812d7))
* **hydra:** Enhance search path appending process ([`f681510`](https://github.com/entelecheia/hyfi/commit/f6815100da661444d39ef128596c8caefc302f0a))

## v1.6.2 (2023-07-22)

### Fix

* **hydra/utils:** Simplify search_path creation ([`a7d5bec`](https://github.com/entelecheia/hyfi/commit/a7d5bec4e4a536ab47092202251cc8c9e0d67e03))
* **hydra:** Optimize search path creation and appending methods ([`26e3d7e`](https://github.com/entelecheia/hyfi/commit/26e3d7ef4a3aabbbd82dc640efe4fedba9668eeb))

## v1.6.1 (2023-07-22)

### Fix

* **hyfi/core:** Optimize search path modifications in _run_hydra function ([`38521fe`](https://github.com/entelecheia/hyfi/commit/38521fe16edecaded5515be4c00218cbc55c782a))

## v1.6.0 (2023-07-22)

### Feature

* **hyfi:** Add hyfi configuration path to search path ([`eceb21f`](https://github.com/entelecheia/hyfi/commit/eceb21f8334ecd0d792d36c6411bf3493272422a))
* **hyfi:** Add hyfi_main to imports and __all__ list ([`3bd4672`](https://github.com/entelecheia/hyfi/commit/3bd4672d6e5008c560c50ce641a304bec8048aea))
* **hydra:** Add main.py and utils.py modules ([`d68c7a8`](https://github.com/entelecheia/hyfi/commit/d68c7a853282faedc1656d799dd94734d07feb7c))
* **hyfi/core/hydra:** Add function get_caller_config_module_path ([`074c538`](https://github.com/entelecheia/hyfi/commit/074c538ab74c5f2680d9ec9a6f2e3be6950bc457))
* **tests:** Add HyFI pipeline datasets tests ([`b2c17b5`](https://github.com/entelecheia/hyfi/commit/b2c17b5febbc5d1d2c25feb74c23a2380521e54a))
* **hyfi/pipe:** Add save, load, and sample dataset functions ([`0f90410`](https://github.com/entelecheia/hyfi/commit/0f904103ec688735c31dc63427f0dd2d83457b4c))
* **hyfi/conf/pipe:** Add load, sample, save dataset configurations ([`63684ed`](https://github.com/entelecheia/hyfi/commit/63684ed8ca89b1c26c30627a66694ac404f130af))

## v1.5.4 (2023-07-21)

### Fix

* **utils:** Add get_caller_module_name method in PKGs class ([`a2e0c8f`](https://github.com/entelecheia/hyfi/commit/a2e0c8fdb667ab71cd527839a6fa213ab1809ffa))
* **hyfi/core:** Add backup functionality and config search path modifications ([`92dc89a`](https://github.com/entelecheia/hyfi/commit/92dc89a83761253c9ed7088e30820eede1050024))

## v1.5.3 (2023-07-21)

### Fix

* **core:** Change default config group value to __init__ ([`4a91f15`](https://github.com/entelecheia/hyfi/commit/4a91f15c7cacb89633af2b48bd587e8a50fd70ab))

## v1.5.2 (2023-07-21)

### Fix

* **main:** Add 'throw_on_compose_failure' argument ([`f1f7e0f`](https://github.com/entelecheia/hyfi/commit/f1f7e0f66e49b6499bd3e2b640ddd7fe8d97f58c))
* **composer/base:** Handle composable config groups more efficiently ([`5eacff2`](https://github.com/entelecheia/hyfi/commit/5eacff20f151f6321d140321824f5930dc7a8f7f))
* **composer:** Add throw_on_compose_failure parameter, improve error handling in _compose method ([`caee9e5`](https://github.com/entelecheia/hyfi/commit/caee9e5a87925b125a8f42d4079e2c759b3ec822))
* **composer:** Streamline config initialization and composition ([`eaddcf3`](https://github.com/entelecheia/hyfi/commit/eaddcf3c3d86eea8652a2ce563fa088bebcd4b40))
* **composer:** Add method to check if  configuration is composable ([`f414c9f`](https://github.com/entelecheia/hyfi/commit/f414c9faf2b24c1c370b7196f94ecc28a02debf3))

## v1.5.1 (2023-07-21)

### Fix

* **composer:** Extract BaseConfig to a separate file ([`8a10dd3`](https://github.com/entelecheia/hyfi/commit/8a10dd3e7d7913ab12e114701483a4fac3e12942))

## v1.5.0 (2023-07-21)

### Feature

* **utils:** Add functions to save and load wordlists ([`14f8bc5`](https://github.com/entelecheia/hyfi/commit/14f8bc5c744952ba7bc62910b403482550d661c9))

## v1.4.0 (2023-07-21)

### Feature

* **hyfi-run:** Enhance CLI with additional options and functionality ([`03229b5`](https://github.com/entelecheia/hyfi/commit/03229b525d5ac62b48175d8f67af6e39a8a66cc6))
* **hyfi:** Refactor and expand functionality ([`5071d52`](https://github.com/entelecheia/hyfi/commit/5071d52256b11f683de3a2fdb55e9f6d85a0cabb))
* **composer:** Add global package list support, add instantiate_config method, add print_config method ([`f98a679`](https://github.com/entelecheia/hyfi/commit/f98a679192756029887c148d585d24ead29f255c))

### Fix

* **hyfi:** Change command configurations ([`990ca36`](https://github.com/entelecheia/hyfi/commit/990ca36b146a7f289cb43a05c5edab1b48d6c295))
* **workflow:** Change 'name' to 'workflow_name' ([`1d9c15a`](https://github.com/entelecheia/hyfi/commit/1d9c15afd8c20337454d5767fb2ce84b67a10565))

## v1.3.1 (2023-07-20)

### Fix

* **hyfi/about:** Improve handling of user configuration path ([`9c535fc`](https://github.com/entelecheia/hyfi/commit/9c535fc5302de27016a887b2efa8db4a10f11d44))
* **__cli__:** Simplify config search path setup ([`2d2e6bd`](https://github.com/entelecheia/hyfi/commit/2d2e6bd0eb24650f07e638ca629b50ac6292c82e))

## v1.3.0 (2023-07-20)

### Feature

* **about:** Add path checker ([`552d1f0`](https://github.com/entelecheia/hyfi/commit/552d1f0649c412a7ddb6023c9ee47fbd6d988ca0))
* **hyfi.core:** Add hydra configuration initialization class and related functions ([`223c133`](https://github.com/entelecheia/hyfi/commit/223c13360ee04a49eb89ac55255dc0a377967eaf))
* **hyfi:** Add user_config_path to about config ([`9f087e9`](https://github.com/entelecheia/hyfi/commit/9f087e98c45d401aef37d461373245494280c7db))
* **about-config:** Add user_config_path property ([`50ea40d`](https://github.com/entelecheia/hyfi/commit/50ea40dc064bcb1e87d0ee9768912df34f41af54))

### Fix

* **hyfi:** Fix searchpath support ([`1bc6323`](https://github.com/entelecheia/hyfi/commit/1bc6323d23bc6f28a5b11e1df40d1ad995d834c7))

### Documentation

* **hyfi/about:** Add user_config_path attribute ([`dca153b`](https://github.com/entelecheia/hyfi/commit/dca153b38f835fc91504659adf5d9900cc845613))
* Rename files in copier and pipe configuration examples ([`3c83044`](https://github.com/entelecheia/hyfi/commit/3c8304417c91de8577cb64176f8241cf89654be9))

## v1.2.14 (2023-07-18)

### Fix

* **hyfi:** Change default copier, add exclude_test_files option, modify path_spec with exclude options, rename conf.yaml to __init__.yaml ([`37f8a14`](https://github.com/entelecheia/hyfi/commit/37f8a147a429be8f4d8b1731e2766893a726bd50))

## v1.2.13 (2023-07-17)

### Fix

* **hyfi:** Improve handling of global project configuration ([`3e1d7ca`](https://github.com/entelecheia/hyfi/commit/3e1d7ca39863e718a977143ba745cafe6b6ffda1))
* **hyfi/main:** Add specific configuration name handling ([`f8ad8dc`](https://github.com/entelecheia/hyfi/commit/f8ad8dc5288a2273014ebc0d056797ed33ceed89))
* **batch:** Add BatchPathConfig to BatchTaskConfig ([`27fb4d6`](https://github.com/entelecheia/hyfi/commit/27fb4d60a9ed355415f4766a4321c76a253a2551))
* **pipeline:** Change task loading logic ([`f75703c`](https://github.com/entelecheia/hyfi/commit/f75703ca2270c83bef1548607c4866bb94e00ce5))
* **hyfi:** Add project setting in cli_main function ([`a1aa5f9`](https://github.com/entelecheia/hyfi/commit/a1aa5f94706225dc77a8f11896418ca5e706b6d5))

## v1.2.12 (2023-07-17)

### Fix

* **task:** Change task_root path in init.yaml ([`79e710c`](https://github.com/entelecheia/hyfi/commit/79e710ce18cc6a3e6fa766cbb353ef6c44e1d433))
* **main:** Simplify and enhance config handling ([`a69c704`](https://github.com/entelecheia/hyfi/commit/a69c704a9e9728cd700a6702cf7817950696ddf3))
* **core:** Add method to get project path in HyfiConfig ([`38b4288`](https://github.com/entelecheia/hyfi/commit/38b42882d9540b516f12e4e834e2b46782ab2e49))
* **path:** Add repr, str methods and get path helper function to BasePathConfig class. ([`7037d29`](https://github.com/entelecheia/hyfi/commit/7037d2923b04886ae6532c50fcee2b24d354b300))

## v1.2.11 (2023-07-17)

### Fix

* **hyfi/utils/envs:** Add functionality to delete environment variables ([`4cf286b`](https://github.com/entelecheia/hyfi/commit/4cf286b84c43fa5ae8af7ee4aed0878fc100eeb1))
* **project:** Rename project name and global workspace name ([`da22cbc`](https://github.com/entelecheia/hyfi/commit/da22cbc729d95716cc4fb452091b844d0b5cb0b4))
* **dotenv:** Change default value of HYFI_GLOBAL_WORKSPACE_NAME ([`6e31dd2`](https://github.com/entelecheia/hyfi/commit/6e31dd2b14ec089f9bf88a0153d52030f9832309))
* **core:** Add .env file support in HyfiConfig ([`23e8ff2`](https://github.com/entelecheia/hyfi/commit/23e8ff2cc8057932f158bad74328ae976cc679bc))
* **hyfi/conf/project:** Add global_workspace_name to __test__.yaml ([`73b1303`](https://github.com/entelecheia/hyfi/commit/73b1303773f3cf31860c17891e59a740ed0a10ec))
* **project:** Update project configuration parameters in __init__.yaml ([`536aa6d`](https://github.com/entelecheia/hyfi/commit/536aa6d5034d12a629e7c8839e875002f0309e44))
* **path:** Modify path configurations in __init__.yaml ([`69c13fe`](https://github.com/entelecheia/hyfi/commit/69c13febe3fd20aa4dd9140d55e7c547a79ce030))

## v1.2.10 (2023-07-16)

### Fix

* **hyfi/core:** Improve package name retrieval in print_about function ([`cd8322e`](https://github.com/entelecheia/hyfi/commit/cd8322e81092828897325b5a43a610b9c012399a))

## v1.2.9 (2023-07-16)

### Fix

* **hyfi:** Add support for additional arguments in about method ([`56a2b05`](https://github.com/entelecheia/hyfi/commit/56a2b05c3270d072b2c26d939be556bf4fd8217e))
* **hyfi/core:** Modify print_about arguments to accept kwargs ([`99c3e1b`](https://github.com/entelecheia/hyfi/commit/99c3e1bef50ec8e19bae1cd4b4adbbf084bb9416))

## v1.2.8 (2023-07-16)

### Fix

* **task:** Replace BatchPathConfig with TaskPathConfig in TaskConfig ([`fdae4f5`](https://github.com/entelecheia/hyfi/commit/fdae4f5335c983e13770d12e57cc7c81ea760645))
* **pipeline:** Change model validation and logging format ([`e00492b`](https://github.com/entelecheia/hyfi/commit/e00492b4bdf7d782d5ad5c47ba0e90918cea6d43))
* **composer:** Enhance data initialization and exclusion in BaseConfig ([`544b58c`](https://github.com/entelecheia/hyfi/commit/544b58cb14a20daa4a0dd3fbf4d013019fd93aa8))
* **workflow:** Replace BaseConfig with BaseModel and add verbose attribute in WorkflowConfig class ([`5fb37fa`](https://github.com/entelecheia/hyfi/commit/5fb37fac9085bdf6a6724f062582246607ab2d97))
* **hyfi:** Update condition checks in run method ([`1ef744a`](https://github.com/entelecheia/hyfi/commit/1ef744a9acc1eec85b1fc1737398b3c3ac399110))
* **hyfi/core/config:** Remove run method from HyfiConfig class ([`d43866b`](https://github.com/entelecheia/hyfi/commit/d43866b359cff7fc6e62e15b2a51b877e70ae0bf))
* **hyfi/conf/workflow:** Add global package in test yaml ([`66c14b3`](https://github.com/entelecheia/hyfi/commit/66c14b3fae3888a910dd19cab9e8ada2b05497bb))
* **workflow:** Remove unused config name ([`d19bed4`](https://github.com/entelecheia/hyfi/commit/d19bed4b7e5ca807690cefa1a9fd12275e9333ea))
* **hyfi:** Improve logging and handling of hyfi instantiation ([`a5698f9`](https://github.com/entelecheia/hyfi/commit/a5698f9ab75befec251067b3e2e94f54d4a97da4))

## v1.2.7 (2023-07-15)

### Fix

* **pipeline/configs:** Add logging information for functions ([`9f7ae60`](https://github.com/entelecheia/hyfi/commit/9f7ae60702cc8ad98437251223dc74bdeafa180c))
* **hyfi:** Change hydra_log_dir in mode/__init__.yaml ([`380a31f`](https://github.com/entelecheia/hyfi/commit/380a31f0cf82bc37c4ea3afdbc4d3cedaa394c28))

## v1.2.6 (2023-07-15)

### Fix

* **task:** Change task_root path to 'workspace' ([`5eb8f75`](https://github.com/entelecheia/hyfi/commit/5eb8f757d8fecd5057dce37d23a08a643120ca33))
* **task:** Change default task_root path ([`6cb8e36`](https://github.com/entelecheia/hyfi/commit/6cb8e36afb0e7cfabcdaabb4eb2d2980bdac624e))
* **batch:** Simplify batch_dir method comments ([`03418c6`](https://github.com/entelecheia/hyfi/commit/03418c689ef68e1416c1c55f555c5b68e69b61a6))
* **task:** Change task_root path in config ([`58a89f0`](https://github.com/entelecheia/hyfi/commit/58a89f05057d214f9166d4fef9b16ab1e4faddda))
* **hyfi:** Modify task_root in path configuration ([`b38d8f8`](https://github.com/entelecheia/hyfi/commit/b38d8f8661cae4ddfb187cc2e5b43ac8ca3b7368))
* **batch:** Update batch_root in configuration ([`51c0c3a`](https://github.com/entelecheia/hyfi/commit/51c0c3ab2a97e469d14f80a4721e259110121971))
* **batch:** Update default batch_root value and improve batch directory creation ([`baa816a`](https://github.com/entelecheia/hyfi/commit/baa816aa7a00918403fa79fe3cd0e0a5e29d1a70))

## v1.2.5 (2023-07-15)

### Fix

* **workflow:** Modify task configuration in __init__.yaml ([`88366e6`](https://github.com/entelecheia/hyfi/commit/88366e679ae227869444343db2a15411b9ab2006))
* **task:** Change task_name from demo-task to __init__ ([`50fcbc8`](https://github.com/entelecheia/hyfi/commit/50fcbc85c00e00fa41926bd56f3ce8d86f69ca96))
* **hyfi/conf/task:** Rename task and batch name settings ([`f15a5c4`](https://github.com/entelecheia/hyfi/commit/f15a5c49d464bcf9e55344c148c0c3b45d8a98cf))
* **hyfi:** Change task name in path configuration ([`42c62bc`](https://github.com/entelecheia/hyfi/commit/42c62bc45ff10a15f9c5e8d3856a9df8bbd878c8))
* **hyfi/path:** Change batch_name default value ([`bf00d0f`](https://github.com/entelecheia/hyfi/commit/bf00d0f31d713ae43b1fa20dc55f387edfb70fb7))
* **dependencies:** Upgrade pydantic to 2.0.3 ([`36b51bd`](https://github.com/entelecheia/hyfi/commit/36b51bdb2652483f9b53bb2fbe8befda4df4d110))

## v1.2.4 (2023-07-14)

### Fix

* **iolibs:** Ensure _path is an instance of Path before calling methods ([`e86407e`](https://github.com/entelecheia/hyfi/commit/e86407e21b2291c47dcb77d0eb46cce3af955cc9))
* **utils/envs:** Enhance find_dotenv function ([`01bd53d`](https://github.com/entelecheia/hyfi/commit/01bd53db20fcec9a84dbbf056fb6e0d683b9ab32))

## v1.2.3 (2023-07-14)

### Fix

* **project:** Add conditional wandb initialization check ([`35103d5`](https://github.com/entelecheia/hyfi/commit/35103d573258a9a290d25376e1f138d157998eb2))

### Documentation

* Add new configurations for various components ([`770348a`](https://github.com/entelecheia/hyfi/commit/770348a901eaf8c8073b46be1074a2d9c29931aa))

## v1.2.2 (2023-07-09)

### Fix

* **project-config:** Add joblib backend initialization and logger debug and warning messages ([`6e699ca`](https://github.com/entelecheia/hyfi/commit/6e699cac9b00e6f280bdfce1184dbbcbc7a68c07))
* **pipeline:** Initialize project before task assignment ([`18b63b6`](https://github.com/entelecheia/hyfi/commit/18b63b6c92a99317a9abdc20869c215460ff90b6))
* **hyfi:** Initialize HyFI in cli_main function ([`8181021`](https://github.com/entelecheia/hyfi/commit/81810212140c5470d9f949d2beecf695e45c751f))

### Documentation

* Add new reference files for various utilities and graphics ([`ca32b9c`](https://github.com/entelecheia/hyfi/commit/ca32b9c88184f22318a5eb13bc62760f47e0e05c))

## v1.2.1 (2023-07-09)

### Fix

* **core:** Rename __global__ to core ([`2e0b418`](https://github.com/entelecheia/hyfi/commit/2e0b41875ad983f917ebdd0c0b34684d13b6a9c2))

### Documentation

* **core:** Rename __global__ to core ([`5aa726b`](https://github.com/entelecheia/hyfi/commit/5aa726b1db9fcef7976f93cc5d9b287882b0b750))

## v1.2.0 (2023-07-09)

### Feature

* **config:** Add run method ([`2d5115e`](https://github.com/entelecheia/hyfi/commit/2d5115e2281dbda6572ee37186dfe91c98955501))

### Fix

* **hyfi:** Add target validation in run function ([`f3be797`](https://github.com/entelecheia/hyfi/commit/f3be797665d133e3e389a0505f78c92d3f589124))
* **graphics:** Add GPUs class for static funcs ([`6162b21`](https://github.com/entelecheia/hyfi/commit/6162b2184df569d7997f4ac1a2822a98d5c625a4))
* **configs:** Fix import of XC ([`37024f3`](https://github.com/entelecheia/hyfi/commit/37024f31e0e3d822f4329b0c2dfe84c19e72c67d))
* **cli:** Handle None config_path correctly ([`81b7f7e`](https://github.com/entelecheia/hyfi/commit/81b7f7e91780aecfaa98afc038daafc51a098edf))
* **main:** Add run function in HyFI class ([`f36da0f`](https://github.com/entelecheia/hyfi/commit/f36da0fd9d579490dd165f89aabf90cd07608afb))
* **config:** Remove print_config option ([`8a2c643`](https://github.com/entelecheia/hyfi/commit/8a2c643ebf125d29b4e7b139f80dec06816c3bd8))
* **config:** Remove print_config flag ([`48fe3ad`](https://github.com/entelecheia/hyfi/commit/48fe3ad4f1a34990e28f921cb37b67aa0785861c))
* **config:** Add print_about method ([`7760ac1`](https://github.com/entelecheia/hyfi/commit/7760ac195b38b215e9b81b7b87877c5c7d8e2620))
* **cli:** Remove unused import and method ([`150d9d5`](https://github.com/entelecheia/hyfi/commit/150d9d580f6796580cf85cf331c23fa5f6277082))

## v1.1.0 (2023-07-08)

### Feature

* **composer:** Add pydantic validation ([`ab42fe1`](https://github.com/entelecheia/hyfi/commit/ab42fe1a2bc9a834d4d1fc81493f368be4bea34d))
* **dependencies:** Add hydra-zen ([`55094ae`](https://github.com/entelecheia/hyfi/commit/55094aec15b5255fd57664b1cd458b7cb1514497))

### Fix

* **cli:** Remove unnecessary comments and conditional statement ([`58add0f`](https://github.com/entelecheia/hyfi/commit/58add0f24c3bb9b2b274e32d2e7f33351322c34e))
* **about:** Handle NoneType for cfg.about ([`92e6207`](https://github.com/entelecheia/hyfi/commit/92e62072be6c1b6833bd95b582567304cd6ae037))

## v1.0.5 (2023-07-05)

### Fix

* **test-batch-task:** Update batch_num in config ([`fc2eae0`](https://github.com/entelecheia/hyfi/commit/fc2eae011dcf21bc4c3a33b87e0ee179ad80c2ce))
* **task:** Update task version ([`973afad`](https://github.com/entelecheia/hyfi/commit/973afad72ec55f4f6008b46fc280c2ffc79c985c))
* **composer:** Register new resolvers for version ([`d4df71d`](https://github.com/entelecheia/hyfi/commit/d4df71dd225ce0ff28fa0347f527b53a986b8d61))

## v1.0.4 (2023-07-04)

### Fix

* **config:** Update set_project_root and set_project_name methods ([`7b3849d`](https://github.com/entelecheia/hyfi/commit/7b3849dd42a18b36057a7d9d4f9bbd49124f3503))
* **task:** Refactor TaskPathConfig class implementation ([`a5b97a3`](https://github.com/entelecheia/hyfi/commit/a5b97a3a410e8a93f4651f1d6655aa0a98c22eb3))
* **dirnames:** Add config file options ([`fc11db7`](https://github.com/entelecheia/hyfi/commit/fc11db78893373b1fe0f4333f259b755713e65c0))
* **path:** Refactor base path configuration ([`ee4d39f`](https://github.com/entelecheia/hyfi/commit/ee4d39f8f6bd33fb60fdce4b3d2084b065e2ac02))
* **path:** Add project_name property ([`dc7162f`](https://github.com/entelecheia/hyfi/commit/dc7162fa099f0be771efcbbecc0e7a3c74a72546))
* **config:** Add reusable config file ([`205cffa`](https://github.com/entelecheia/hyfi/commit/205cffa5871a95a97129991c6f37b09311e4cbbb))
* **batch:** Move config_dir to the correct position ([`76e5001`](https://github.com/entelecheia/hyfi/commit/76e500104286b9a99f7562039b85bbc1d1a61fb6))
* **dependencies:** Upgrade joblib to ^1.3.1 ([`ee8bfbb`](https://github.com/entelecheia/hyfi/commit/ee8bfbb662e13ccf254ab7e178579a9f4f06df40))

## v1.0.3 (2023-07-04)

### Fix

* **tests:** Fix batch task configuration ([`16acf17`](https://github.com/entelecheia/hyfi/commit/16acf173f75200170b49ba17739c77d3b00f2331))
* **batch:** Improve config handling ([`ec03733`](https://github.com/entelecheia/hyfi/commit/ec037333789dab1bbd7a59f807a0b5ebbbf4a6c2))
* **BaseConfig:** Add subconfig initialization ([`6e84c4e`](https://github.com/entelecheia/hyfi/commit/6e84c4e69acea6fa8cf04dc65eac2bfa554515e5))

## v1.0.2 (2023-07-04)

### Fix

* **joblib:** Optimize test_batcher.py ([`d15c426`](https://github.com/entelecheia/hyfi/commit/d15c42663ae75a6adc660831e1457b80c8fa5e69))
* **batcher:** Fix logging formatting ([`484c06b`](https://github.com/entelecheia/hyfi/commit/484c06b30c51fc150b480adb342da9345c63cbfa))
* **config:** Remove unnecessary configuration options in JobLibConfig ([`48050a7`](https://github.com/entelecheia/hyfi/commit/48050a7fc57fe5fb954db955b8c0b023175c7e52))
* **joblib:** Update configuration settings ([`5c4a6a1`](https://github.com/entelecheia/hyfi/commit/5c4a6a120e7adff41926b43057bf0e8a53e7db63))

## v1.0.1 (2023-07-04)

### Fix

* **workflow:** Fix task configuration parsing ([`20a582c`](https://github.com/entelecheia/hyfi/commit/20a582c1d77ac63a630b1dd8c43697ce5d491d6b))
* **pipeline:** Improve pipeline configuration handling ([`af30e4d`](https://github.com/entelecheia/hyfi/commit/af30e4d6603db4951d124a9481037abea25462e2))
* **dotenv:** Update check_and_set_values method ([`7a94d24`](https://github.com/entelecheia/hyfi/commit/7a94d2487c5fabc8b22efdeae99edda29819b37d))

## v1.0.0 (2023-07-04)

### Feature

* **task:** Add task dirnames config ([`7c486e4`](https://github.com/entelecheia/hyfi/commit/7c486e4be2108d0c0ce64cc0a4e94a446a128358))
* **path:** Add DirnamesConfig class and default directory names ([`59b312f`](https://github.com/entelecheia/hyfi/commit/59b312f72212963b750fca4da9f23d3eae12d233))
* **path:** Add directory names configuration file ([`274e841`](https://github.com/entelecheia/hyfi/commit/274e84173f030c2ec02ac65b40d4cc7ccf88c989))
* **dependencies:** Update pydantic to version 2.0.0 ([`964c2ef`](https://github.com/entelecheia/hyfi/commit/964c2ef729090985e4441a13545967ba2a50d42f))

### Fix

* **joblib:** Fix stopping distributed framework ([`8825996`](https://github.com/entelecheia/hyfi/commit/882599651a486bd88c7a526e99fc04a8a0e8d00c))
* **config:** Improve model data validation ([`b774d25`](https://github.com/entelecheia/hyfi/commit/b774d25253b928e715ec7939eefaf06b3340e29e))
* **composer:** Update XC.instantiate method ([`3a08f99`](https://github.com/entelecheia/hyfi/commit/3a08f9984ec1843853198f564f813e8feaea168e))
* **hyfi-composer:** Fix retrieving package source ([`33b5037`](https://github.com/entelecheia/hyfi/commit/33b5037315300f179c7a16ccf4c193c28d6c5854))
* **docs:** Update variable names in examples ([`43d04eb`](https://github.com/entelecheia/hyfi/commit/43d04eb8dbdcd26219a8f7ce7c9450d5786b8df5))

### Breaking

* support pydantic v2 ([`964c2ef`](https://github.com/entelecheia/hyfi/commit/964c2ef729090985e4441a13545967ba2a50d42f))

### Documentation

* **task:** Add batch functionality ([`d687528`](https://github.com/entelecheia/hyfi/commit/d687528426682bbb2a34ac5c831fada4c472508d))
* **task:** Add hyfi.task documentation ([`5c435fe`](https://github.com/entelecheia/hyfi/commit/5c435fee0ea0726510335c5f175c324d75263c79))
* **task:** Add batch documentation ([`cf613c9`](https://github.com/entelecheia/hyfi/commit/cf613c9e20294fcdd5f1ae44900470f985d6c509))
* **docs:** Add project reference page ([`cb1487f`](https://github.com/entelecheia/hyfi/commit/cb1487fdc589dd311e694e9d4a0a17fe7388c9e2))
* **pipeline:** Add configs ([`0944da5`](https://github.com/entelecheia/hyfi/commit/0944da503e45a48187c8447da043bdca40cd2dac))
* **module:** Add hyfi.module documentation ([`fb3d6b2`](https://github.com/entelecheia/hyfi/commit/fb3d6b2c04b3d4d82dc766bef863784b29f76272))
* **graphics:** Add hyfi.graphics documentation ([`4e8b54d`](https://github.com/entelecheia/hyfi/commit/4e8b54d13315b980c83792680943ef8ed3e883ce))
* **pipeline:** Add config documentation ([`ca0653b`](https://github.com/entelecheia/hyfi/commit/ca0653bf8a1d1ef587c2ec3c0795636ac02d86c4))
* Create `hyfi.pipe` reference documentation ([`71575c3`](https://github.com/entelecheia/hyfi/commit/71575c3c8d634c8c2e9deff643a2f421bcca4a46))
* **dotenv:** Add configuration class for environment variables in HyFI ([`f5493ba`](https://github.com/entelecheia/hyfi/commit/f5493ba01d1767002608ec59c3a40d64ee05b707))
* **copier:** Add copier documentation ([`0bca38d`](https://github.com/entelecheia/hyfi/commit/0bca38d24590cf50fe37ba50453723e14e11c552))
* **batch:** Add hyfi.batch documentation ([`b75dd3f`](https://github.com/entelecheia/hyfi/commit/b75dd3f0786ea8a46767c9e85381318bb8bb50a5))
* **utils:** Update docstrings ([`cac53f8`](https://github.com/entelecheia/hyfi/commit/cac53f83410443ca21f5dd0dea56e263321c6c46))
* **joblib:** Add batcher documentation ([`8d74675`](https://github.com/entelecheia/hyfi/commit/8d74675daab763a11f3df8a95036994656e5cdcf))
* **joblib.batch:** Add apply function ([`9c29ef6`](https://github.com/entelecheia/hyfi/commit/9c29ef60ecadc512d80684e28f5ed43ea261b028))
* **hyfi.joblib.batch:** Add apply_batch method ([`6f17119`](https://github.com/entelecheia/hyfi/commit/6f17119de614b049f36316bef7c81f971ebd3681))
* **joblib:** Add documentation for hyfi.joblib ([`d955315`](https://github.com/entelecheia/hyfi/commit/d955315378bcb963b91ff65ceff8db0c4af8c6f5))

## v0.16.3 (2023-07-01)

### Fix

* **composer): Fix type annotations in update method; fix(composer:** Return filepath as string in save_config_as_json method ([`7bb3849`](https://github.com/entelecheia/hyfi/commit/7bb3849327db551f46eac2c5ff5acaeb4672b245))
* **utils:** Fix lower_case_with_underscores function ([`56ea30b`](https://github.com/entelecheia/hyfi/commit/56ea30b86c4d3faf6d9366e65f40b8c83ec84da2))

### Documentation

* **composer:** Update docstring in BaseConfig ([`5106221`](https://github.com/entelecheia/hyfi/commit/5106221ffcbbc02e20e6f9d397e45827e0c0a40e))

## v0.16.2 (2023-06-30)

### Fix

* **task:** Simplify load_config method ([`997cb98`](https://github.com/entelecheia/hyfi/commit/997cb988f07a5fa5aacde32e7ba4bbb445dae78f))
* **composer:** Improve config export and saving methods ([`d77eea2`](https://github.com/entelecheia/hyfi/commit/d77eea266cf8fd9a7088bff60de5d3f4bf5ce82c))

## v0.16.1 (2023-06-30)

### Fix

* **batch:** Update BatchConfig initialization logic ([`a4b8080`](https://github.com/entelecheia/hyfi/commit/a4b8080e70256a6332ecc94139d3d3db3a52371f))

## v0.16.0 (2023-06-30)

### Feature

* **pipeline:** Update initial object configuration ([`d695ca2`](https://github.com/entelecheia/hyfi/commit/d695ca2c1b6901f34800c13dccb21feda45cd472))
* **task:** Add new pipelines ([`ab2d1bb`](https://github.com/entelecheia/hyfi/commit/ab2d1bb797db937f62a90f609c7a1834a86fa3cd))
* **pipeline:** Add __test_general__.yaml ([`893ee20`](https://github.com/entelecheia/hyfi/commit/893ee20d1f948ec58f9b8e31fa6f9eda8c49d76d))
* **pipeline:** Update run_pipeline method ([`1498128`](https://github.com/entelecheia/hyfi/commit/1498128390190e243108ef570ec35fbf78e0c5c3))
* **pipe:** Add general_instance_methods and general_external_funcs ([`efbae91`](https://github.com/entelecheia/hyfi/commit/efbae91599506ffec13ac893452d7404889c1dfe))
* **pipeline:** Add use_self_as_initial_object ([`cb7f5db`](https://github.com/entelecheia/hyfi/commit/cb7f5db17a49b4acde7daab84e009b9e91b00b29))
* **conf:** Add __general_instance_methods__.yaml ([`04cd575`](https://github.com/entelecheia/hyfi/commit/04cd5751038e0eba13ec8bdeebd3b98d42f88f44))
* **pipe:** Add general external functions ([`5e6db50`](https://github.com/entelecheia/hyfi/commit/5e6db5021c03e894f26a48752da196d9f6b1d1c8))

### Fix

* **pipeline:** Fix use_task_as_initial_object typo ([`88c2561`](https://github.com/entelecheia/hyfi/commit/88c25617afe4e1ba3e2f53a39824daffbba9ecc0))
* **pipeline:** Update initial object usage ([`c222f45`](https://github.com/entelecheia/hyfi/commit/c222f459312b395f206bd4a1a479223bad812536))
* **hyfi/pipeline:** Fix task configuration naming ([`85317cf`](https://github.com/entelecheia/hyfi/commit/85317cf74075e1a7f5e582c0233e0ef16f1b1182))
* **dotenv:** Fix variable name in DotEnvConfig ([`09de6f4`](https://github.com/entelecheia/hyfi/commit/09de6f4dd34a1d40a845a1834883aef166e391c0))
* **conf:** Fix config file names ([`354c9b4`](https://github.com/entelecheia/hyfi/commit/354c9b48250ee283f00940c640e840ecce3edc57))

## v0.15.1 (2023-06-28)

### Fix

* **pipeline:** Fix argument name in get_RCs method ([`0698f5a`](https://github.com/entelecheia/hyfi/commit/0698f5a01110dad1c21e7d6e24070efc6a443529))

### Documentation

* Update reference global and path pages, rename about and main pages to index.md ([`043aa23`](https://github.com/entelecheia/hyfi/commit/043aa2316ecf3db2a05ee6aa194ebc85b9a06f03))
* **configurations:** Add path and project configurations with init, task, batch, and test files included ([`f0aa8a6`](https://github.com/entelecheia/hyfi/commit/f0aa8a6e4941223891fb4096bc6acbc9614b5077))
* Add config.yaml documentation ([`f0af38a`](https://github.com/entelecheia/hyfi/commit/f0af38a3734916c4c92a6ac93cb1249296cdb012))
* **config:** Improve method documentation ([`fd6dbf2`](https://github.com/entelecheia/hyfi/commit/fd6dbf26f4387c50376e417974a4f63b3ce0e4cc))
* **composer:** Simplify XC class, add docstrings ([`b5d8804`](https://github.com/entelecheia/hyfi/commit/b5d880478c8533a9d7e2f396b492cbf04dbe9251))
* **composer:** Add documentation for ensure_kwargs method ([`389baa3`](https://github.com/entelecheia/hyfi/commit/389baa3d5398161645aa6fefa419165c149deee3))
* **composer:** Clarify method docstrings and add missing args and returns information ([`db5d260`](https://github.com/entelecheia/hyfi/commit/db5d260a7fa68e21b64da52a639c82343fb7cdbb))
* **composer:** Clarify comments and docstrings ([`cd92334`](https://github.com/entelecheia/hyfi/commit/cd9233444d6bfb21821acc966e946261cc02a052))
* Rename composer.md to composer/index.md and add extended.md ([`a662885`](https://github.com/entelecheia/hyfi/commit/a662885739705898f32e46c2322c0df463cd66f6))

## v0.15.0 (2023-06-27)

### Feature

* **cli:** Add test for command 'run_workflow' ([`9658d12`](https://github.com/entelecheia/hyfi/commit/9658d12ba2bed52fbb24ececb8882ebd0e6444a5))
* **workflow:** Add WorkflowConfig class to __init__.py ([`aa23b50`](https://github.com/entelecheia/hyfi/commit/aa23b5094afacbb483fc79b65ae572b6b7f56a8c))
* **pipeline:** Add workflow support ([`6114f28`](https://github.com/entelecheia/hyfi/commit/6114f28e582cd47d466f455a286c79f78e844047))
* **workflow:** Add function to run the pipelines specified in a workflow ([`1382f3c`](https://github.com/entelecheia/hyfi/commit/1382f3c54f159b0839d5aa57f3db46cf1a8f1f71))
* **cmd:** Add run_workflow.yaml ([`e17fc5a`](https://github.com/entelecheia/hyfi/commit/e17fc5a77018d32b5e41ddc8ff93f6602cf29ddc))
* **cli:** Add run workflow command ([`7035e1d`](https://github.com/entelecheia/hyfi/commit/7035e1de4707aa022327815b5c94a766e6fa1711))
* **pipeline:** Add support for project config in task pipeline testing ([`db034a4`](https://github.com/entelecheia/hyfi/commit/db034a41ca565404ac90516505aaab31b8fc7642))

### Fix

* **cli:** Add project parameter to run_task method ([`ced932b`](https://github.com/entelecheia/hyfi/commit/ced932b4eb9524a03438dc27a11b9fe10e80741d))

### Documentation

* **pipeline:** Add docstrings and improve readability ([`d3c80b7`](https://github.com/entelecheia/hyfi/commit/d3c80b703200964a7487faa81f2db7d73806413b))
* **cli:** Add docstrings to run_copy and run_workflow functions ([`34f17dc`](https://github.com/entelecheia/hyfi/commit/34f17dce34f112da7f0ec3b8460574432a98fcf4))
* **pipeline:** Add initial documentation ([`9286832`](https://github.com/entelecheia/hyfi/commit/9286832470d6a8df9f39a47443e9b154371376c4))

## v0.14.2 (2023-06-26)

### Fix

* **configs:** Add use_pipe_obj and return_pipe_obj flags ([`6b10ceb`](https://github.com/entelecheia/hyfi/commit/6b10ceb34be48e74b3fe04775d367049d6fe1735))
* **pipe:** Improve handling of data input and output ([`3d217a0`](https://github.com/entelecheia/hyfi/commit/3d217a0234363399d7d2735091861b9cfada887b))
* **conf:** Update pipe configuration with new options ([`a0d1297`](https://github.com/entelecheia/hyfi/commit/a0d1297af783ffde3f8e01b2f6f8589e49bb457c))

## v0.14.1 (2023-06-26)

### Fix

* **configs:** Rename RunConfig to PipeConfig, add _pipe_ and _run_ keys ([`d732cbd`](https://github.com/entelecheia/hyfi/commit/d732cbd967a788d0a5f9951cd8484f04ea8795dc))
* **pipeline:** Update get_pipe_func call in PIPELINEs class ([`6354d57`](https://github.com/entelecheia/hyfi/commit/6354d572a32487959e94f492083fff5a4a74ee49))
* **pipe:** Rename DataframeRunConfig to DataframePipeConfig ([`7d24e76`](https://github.com/entelecheia/hyfi/commit/7d24e7624a06f59f5f901a5b08f24b8b7bb25a87))
* **conf:** Modify dataframe_instance_methods.yaml defaults key ([`6bda0c1`](https://github.com/entelecheia/hyfi/commit/6bda0c1be35d433a96e65c632e3f8f1e52e1a4cb))
* **pipe:** Modify dataframe external functions default configuration ([`afbaa52`](https://github.com/entelecheia/hyfi/commit/afbaa52e32b202cf2b352227afb33a7ca7a3840c))

## v0.14.0 (2023-06-26)

### Feature

* **pipeline:** Add task configuration to RunConfig object ([`9c16b6a`](https://github.com/entelecheia/hyfi/commit/9c16b6a9025673c758b0802a17055b0f8e0577c0))
* **pipeline:** Add support for task-specific pipelines ([`8c4a595`](https://github.com/entelecheia/hyfi/commit/8c4a59550e51449f69bd8e44b1165b94b67b96ba))
* **task:** Add new method to create TaskConfig objects. ([`3742b90`](https://github.com/entelecheia/hyfi/commit/3742b902826ab624743981d020ccc91c1490f976))
* **pipe:** Add function to preprocess ESG ratings data ([`58773c3`](https://github.com/entelecheia/hyfi/commit/58773c35ee4b7d5b6e0e7a3d66bcce171f5c3024))
* **preprocessing:** Add test_preprocessing.yaml configuration file ([`0190245`](https://github.com/entelecheia/hyfi/commit/0190245e8ae33cf31d77b6c685416484e34a878a))
* **pipe:** Add save_dataframes.yaml config file ([`c11fbdc`](https://github.com/entelecheia/hyfi/commit/c11fbdc4f1803c8572a529e3c151ba29371bad95))

### Fix

* **cli:** Add validation for missing task configuration before running HyFi task pipelines ([`a2711cf`](https://github.com/entelecheia/hyfi/commit/a2711cf46b2cc3946f00f37a34987e1a9b13277d))
* **tests:** Fix project root path in test PathConfig ([`32d49e1`](https://github.com/entelecheia/hyfi/commit/32d49e1d73e84ebbbb0b9ce357a30ca700febff0))

## v0.13.0 (2023-06-26)

### Feature

* **pipeline:** Add a PipelineConfig class and PIPELINEs class with methods for running a pipeline, running a pipe, and getting running configs from a list. ([`6a4a321`](https://github.com/entelecheia/hyfi/commit/6a4a32112ad083900fe636da0eb2c438df052bb4))
* **pipeline:** Add "compose_as_dict" method to allow composing configuration as a dictionary ([`09ad137`](https://github.com/entelecheia/hyfi/commit/09ad137995a50be06185fe3e2f7ca5dbd252f9f7))
* **pipe:** Add load_dataframes.yaml configuration file ([`98b9e59`](https://github.com/entelecheia/hyfi/commit/98b9e59d0843ccfffcb36eac90da9b982c0b9449))
* **conf:** Add running config file ([`e604129`](https://github.com/entelecheia/hyfi/commit/e60412991fe38530481a4a53818e48c2aaba386b))
* **pipeline:** Add __test__.yaml configuration for testing pipeline ([`01a1957`](https://github.com/entelecheia/hyfi/commit/01a195780681ec35f784dab50d4d3af1520de595))
* **pipeline:** Add configs module with BaseRunConfig, RunningConfig, Steps, Pipelines, Tasks, RunConfig, DataframeRunConfig, and PipeConfig ([`2c39ae2`](https://github.com/entelecheia/hyfi/commit/2c39ae2f071ddeaed648e15d83ad1ea2bf96f1d3))
* **joblib:** Add BATCHER class and apply method ([`bf89e1d`](https://github.com/entelecheia/hyfi/commit/bf89e1d9708ab9bc5d22c5b42cc5568c3979a73d))

### Fix

* **utils:** Fix import statement in test_utils_env.py ([`a9ed751`](https://github.com/entelecheia/hyfi/commit/a9ed751dc365fb1fbe403b666fecfb8a69574157))
* **utils:** Fix class naming and update method names for clarity ([`1a3f559`](https://github.com/entelecheia/hyfi/commit/1a3f559162af98dbc8811641a68ecfd6e386e122))
* **joblib:** Update pipe function to use BATCHER instead of PIPE in HyFI class ([`cd3c94c`](https://github.com/entelecheia/hyfi/commit/cd3c94cbeb15c830d20419d6cb92c5fee664d86c))

## v0.12.3 (2023-06-23)

### Fix

* **datasets:** Add save_dataframe method ([`9633738`](https://github.com/entelecheia/hyfi/commit/9633738481d2dc8c3d8434fca7d8e059247f0ac9))

## v0.12.2 (2023-06-21)

### Fix

* **cli:** Rename print_resolved_config to resolve ([`388130a`](https://github.com/entelecheia/hyfi/commit/388130a27276703f7636f9c06b071581f3793796))
* **config:** Rename print_resolved_config to resolve ([`7742516`](https://github.com/entelecheia/hyfi/commit/77425165c7138780cdd1494f8fef3be013572fe2))
* **config:** Update mode config to use resolve instead of print_resolved_config ([`1a7792a`](https://github.com/entelecheia/hyfi/commit/1a7792a76d1c5be209659e8c6234ead9a4246616))

## v0.12.1 (2023-06-21)

### Fix

* **pipe:** Fix incorrect value in PipeConfig init method ([`dc9018d`](https://github.com/entelecheia/hyfi/commit/dc9018d2ca620ef261baf9c3a5d4ce08b4aa3205))
* **main:** Add optional arguments to joblib and dotenv methods and add pipe_config method ([`2879e49`](https://github.com/entelecheia/hyfi/commit/2879e490df879b306f9fb908c27ce5bbe11a9613))

## v0.12.0 (2023-06-21)

### Feature

* **main:** Add reinit option in hyfi constructor ([`b521054`](https://github.com/entelecheia/hyfi/commit/b521054e4b2213a6365892eb6e74eac96c5016a4))
* **config:** Add "reinit" parameter to initialize method ([`57e93cb`](https://github.com/entelecheia/hyfi/commit/57e93cb01ec7034112f8cef37790daa8f85c24b7))
* **pipe:** Add lambda configuration file ([`9206107`](https://github.com/entelecheia/hyfi/commit/9206107a875d044398dc0e48504b35a2269c6f1f))
* **composer:** Add support for new special key TYPE ([`2de9cfd`](https://github.com/entelecheia/hyfi/commit/2de9cfd06a22abb9a507658f59fd8481cc01b006))
* **pipe:** Add PIPE and PipeConfig classes with apply and pipe methods. ([`df2c032`](https://github.com/entelecheia/hyfi/commit/df2c0321dd97fb3dc79576f24c188328cad47af0))
* **pipe:** Add pipeline functions for dataframe operations ([`9d5f6e7`](https://github.com/entelecheia/hyfi/commit/9d5f6e77ffac6885c8759bde6d84416302831108))
* **pipe:** Add initial configuration file for pipe function ([`f205e70`](https://github.com/entelecheia/hyfi/commit/f205e7083f819bad266279f05804cade3d69fb05))

### Fix

* **init:** Set reinit to True ([`be235ba`](https://github.com/entelecheia/hyfi/commit/be235ba62e07630a4407cbefaed723b2ca19afb0))
* **config:** Set "reinit" to True in HyfiConfig class ([`a393cfc`](https://github.com/entelecheia/hyfi/commit/a393cfccebd10bd68422f557ad5c0927ac3b5bb8))
* **pipe:** Add error handling for missing method in config ([`5fe151f`](https://github.com/entelecheia/hyfi/commit/5fe151f4a1b58d80b77c05788aeb9ad1bca97de4))
* **pipe:** Update apply_to default value in PipeConfig class ([`90234f1`](https://github.com/entelecheia/hyfi/commit/90234f15bf4498b993bf2952c72df1d110cd765a))
* **dependencies:** Add batcher instance to global init file ([`5af5726`](https://github.com/entelecheia/hyfi/commit/5af57269eafe0888085beabab89037d0e266f2d1))
* **dependencies:** Add joblib 1.2.0 ([`cf06051`](https://github.com/entelecheia/hyfi/commit/cf060517df4a7b4545c2040ca1045a84e1231ab7))

## v0.11.0 (2023-06-21)

### Feature

* **datasets:** Add support for loading and concatenating dataset-like objects and dataframes. ([`a6540e1`](https://github.com/entelecheia/hyfi/commit/a6540e134b92194466a3b2ec99af1c2d0b3ddded))

### Fix

* **datasets:** Add condition to concatenate datasets properly ([`ebc3b3e`](https://github.com/entelecheia/hyfi/commit/ebc3b3e88066999003dfcff2f32628e9ea6cc5b3))
* **datasets:** Change load_data method arguments ([`7322eb6`](https://github.com/entelecheia/hyfi/commit/7322eb667846018d68d4ced0f9d604fa74cc3103))

## v0.10.1 (2023-06-20)

### Fix

* **config:** Update version in global config ([`7dc72cc`](https://github.com/entelecheia/hyfi/commit/7dc72cc079e610f7d898bc65c7aabc5c77aa21f9))
* **config:** Update version in about information ([`c00134a`](https://github.com/entelecheia/hyfi/commit/c00134a42366ae529a903b1f9730d16e0ec47e9d))

## v0.10.0 (2023-06-20)

### Feature

* **composer:** Rename hydra to composer and move main.py to extended.py ([`0defc55`](https://github.com/entelecheia/hyfi/commit/0defc55470b6e037175f7f84f4b8674fe5eb7d51))

### Documentation

* **readme:** Fix formatting in README.md ([`3c3c309`](https://github.com/entelecheia/hyfi/commit/3c3c30961d7afce629da8053759363e433040fc4))

## v0.9.1 (2023-06-20)

### Fix

* **envs:** Add check_and_set_osenv method. ([`c21af9a`](https://github.com/entelecheia/hyfi/commit/c21af9ac1cded179f048009fba5045d0745c79f9))

## v0.9.0 (2023-06-20)

### Feature

* **iolibs:** Add cached_path method for caching URLs and files locally ([`2ee9a39`](https://github.com/entelecheia/hyfi/commit/2ee9a39d78d17b4c3dec164baed1e5b5284b1842))
* **iolibs:** Add method to get file modified time ([`5ec4e36`](https://github.com/entelecheia/hyfi/commit/5ec4e3671b18021f4ce789c944d9aeb4c283d7a2))
* **datasets:** Add load_dataset method for easily loading datasets from local or Hugging Face Hub directories or repositories. ([`54b7075`](https://github.com/entelecheia/hyfi/commit/54b707502ba92f1341247df86a99e90ba5eee66f))

### Fix

* **main:** Fix typo in Envs.get_osenv call ([`49e98e6`](https://github.com/entelecheia/hyfi/commit/49e98e65f140c85820db4b492aa290eb1ad52b8c))
* **utils:** Import statement from modified Libs module ([`0e8901b`](https://github.com/entelecheia/hyfi/commit/0e8901bffebfc2e507dac3f1ff62c45c84c06294))
* **libs:** Add Libs module and move relevant functions to it ([`185651e`](https://github.com/entelecheia/hyfi/commit/185651e271c4dd9954191bd89246ec12a4c9d04e))

## v0.8.2 (2023-06-19)

### Fix

* **config:** Change log level of no config group message ([`8d29a6f`](https://github.com/entelecheia/hyfi/commit/8d29a6f69178130914c461ae159532c5199809af))
* **logging:** Change logger level to debug in config file ([`23a5021`](https://github.com/entelecheia/hyfi/commit/23a5021faa6cb839d460d3db0051af06de1991f4))

## v0.8.1 (2023-06-19)

### Fix

* **dependencies:** Update pandas, numpy, filelock, and huggingface-hub versions. ([`47ec1cb`](https://github.com/entelecheia/hyfi/commit/47ec1cbd25df8c24c3accb3f665bf6a928289542))
* **dependencies:** Update logger.debug message in gpu.py ([`4eb9e6e`](https://github.com/entelecheia/hyfi/commit/4eb9e6ecd8c14832e78d331ea3e1df5970c615a4))

## v0.8.0 (2023-06-18)

### Feature

* **path:** Add TaskPathConfig model class and properties ([`316f5ff`](https://github.com/entelecheia/hyfi/commit/316f5fffde28d92dd4ca8f85dd386bd54583a7f1))

### Fix

* **utils/gpu:** Set proper exception for CUDA device not found error ([`220c114`](https://github.com/entelecheia/hyfi/commit/220c114efcf3392e1802221b5121932229cc2763))

## v0.7.2 (2023-06-17)

### Fix

* **graphics:** Load_image function now supports filepath input ([`e13aebd`](https://github.com/entelecheia/hyfi/commit/e13aebd66158e2b5d3b43e1c6a9c2bf22c6aae91))

## v0.7.1 (2023-06-17)

### Fix

* **fileutils:** Handle empty filename_patterns and filename when saving data ([`3e1d450`](https://github.com/entelecheia/hyfi/commit/3e1d450c7e726302f2c9169248472f18960b3218))
* **config:** Fix import of __search_package_path__ in hydra/main.py ([`e07d932`](https://github.com/entelecheia/hyfi/commit/e07d932ac69c68b48e8cee5c8554087462efec7c))

## v0.7.0 (2023-06-16)

### Feature

* **hyfi:** Add run_task command configuration file ([`1a489f9`](https://github.com/entelecheia/hyfi/commit/1a489f94d630afa131765f706006a055b71dbd13))
* **cli:** Add run_task command ([`45da824`](https://github.com/entelecheia/hyfi/commit/45da824fba4a3741e684057e120d41f5a1029469))
* **batch:** Implement BatchTask with save/load config functionality ([`ad197a1`](https://github.com/entelecheia/hyfi/commit/ad197a1ebb68f0197467562931779b0c4d4a8fb6))
* **task:** Add BaseTask class for task configuration and management ([`7ff563d`](https://github.com/entelecheia/hyfi/commit/7ff563d96de2af2d770cfa6239770177ad23371b))

### Fix

* **cli:** Handle case when no copier configuration is found. ([`beebfdc`](https://github.com/entelecheia/hyfi/commit/beebfdcaaa81502ce2c0be7b1cdc3591d4721147))
* **docs:** Update example to use correct configuration path ([`6e53aa6`](https://github.com/entelecheia/hyfi/commit/6e53aa6082c8b30b935a2b93a11a2bbb0e292575))

### Documentation

* **reference:** Add about page ([`0e9ca1f`](https://github.com/entelecheia/hyfi/commit/0e9ca1f59c2c65738fc3c33955c2967c4468b06c))

## v0.6.2 (2023-06-16)

### Fix

* **cli:** Add options for exclude, skip_if_exists, overwrite, dry_run, and verbose in 'cc' command ([`228fab4`](https://github.com/entelecheia/hyfi/commit/228fab43b7796b974a213e58ae4b90e7fd320a9f))

## v0.6.1 (2023-06-16)

### Fix

* **tests:** Update global_hyfi_root path in test_init_workspace function ([`ecb2e73`](https://github.com/entelecheia/hyfi/commit/ecb2e737267c03c14eaa498bab0f46c94f6ad304))

## v0.6.0 (2023-06-15)

### Feature

* **docs:** Add mkdocs-click extension ([`d1220ab`](https://github.com/entelecheia/hyfi/commit/d1220ab5b17ee035b89cdf9f3bdb5dde5e5f8eb7))
* **hyfi:** Refactor copy command to use Copier class ([`484835c`](https://github.com/entelecheia/hyfi/commit/484835ceec4b7b4a9d12c98230fb2fe1b2affe43))
* **cli:** Add command line interface (CLI) with 3 commands: cc, about, and sc ([`303cc7b`](https://github.com/entelecheia/hyfi/commit/303cc7b02dc9b790923b9ec235ac274b1af347dc))

### Fix

* **utils:** Fix import statements and update path for source directory in Copier class ([`946976a`](https://github.com/entelecheia/hyfi/commit/946976acdd570394eeec63b65fda190b73e0eeab))
* **env:** Fix compose, init functions for configs ([`f1e2d5a`](https://github.com/entelecheia/hyfi/commit/f1e2d5a1e9fb0b98db1155e3d48f5e03980d00d7))
* **config:** Add support for setting project description in init_workspace method ([`c32b171`](https://github.com/entelecheia/hyfi/commit/c32b1717a3b85897c6783e292c3537bdd805284e))

### Documentation

* **cli:** Add click.md for CLI documentation ([`2f205ca`](https://github.com/entelecheia/hyfi/commit/2f205ca41b1431ba8d3d8c35071c36920c4773b5))
* **cli:** Update documentation to clarify use of hydra package. ([`8b22ce4`](https://github.com/entelecheia/hyfi/commit/8b22ce447909b3c7b5bb721f711c280a114253eb))

## v0.5.1 (2023-06-14)

### Fix

* **env:** Fix import statement in __version__ function ([`2c3bf84`](https://github.com/entelecheia/hyfi/commit/2c3bf84423d93024838aa3ea09948431ad35a684))
* **main:** Fix imports in main.py file ([`cba94f2`](https://github.com/entelecheia/hyfi/commit/cba94f2a91d76fb3d6e65117f5137c8e05308aa0))

### Documentation

* **config:** Add hyfi.config.path documentation ([`f7ea8ce`](https://github.com/entelecheia/hyfi/commit/f7ea8ce42c1e0566b1e295842bb53cd2fa3b0df6))

## v0.5.0 (2023-06-12)

### Feature

* **tests:** Add test for PathConfig class in hyfi.env module ([`ca87ba4`](https://github.com/entelecheia/hyfi/commit/ca87ba43d9b82e8094e30f5a9379cd0d141cc183))
* **reference:** Add hyfi.main documentation ([`4dee766`](https://github.com/entelecheia/hyfi/commit/4dee766e9bd79d98ddd204a60d7c85e4abe92637))
* **utils:** Add method to expand POSIX variables ([`36c80c2`](https://github.com/entelecheia/hyfi/commit/36c80c2643b373311619fe60695384886df6b4e0))
* **docs:** Add usage documentation ([`968430e`](https://github.com/entelecheia/hyfi/commit/968430e1c302c08f75de7deec725da1ada841a88))
* **utils:** Add unittest for expand_posix_vars function ([`d960a8f`](https://github.com/entelecheia/hyfi/commit/d960a8f84c650ca0a701dc7464306031c8d70309))
* **env:** Add ability to retrieve the value of an environment variable ([`a9b78f7`](https://github.com/entelecheia/hyfi/commit/a9b78f7c6a0dc35d8dfd299c16de2d87f34e78e4))

### Fix

* **dependencies:** Add ipywidgets to ipython extra ([`7d1f955`](https://github.com/entelecheia/hyfi/commit/7d1f955ab942b22491ad49e9d530313051aca6ae))
* Apply the latest template ([`51b6824`](https://github.com/entelecheia/hyfi/commit/51b68243b23f612c9fb4a49c4298358793763d82))

## v0.4.0 (2023-05-06)
### Feature
* **env:** Add OPENAI_API_KEY to dotenv ([`a4238db`](https://github.com/entelecheia/hyfi/commit/a4238db21d1330e92d6da968f12770776c51dd4c))

## v0.3.5 (2023-05-05)
### Fix
* **types:** Sort import ([`40d7019`](https://github.com/entelecheia/hyfi/commit/40d70193dafb4c226a10e1b39e89dec6ed293521))

## v0.3.4 (2023-05-05)
### Fix
* **copier:** Add filetypes parameter for copying specific filetypes ([`84f6163`](https://github.com/entelecheia/hyfi/commit/84f61631f1d8a79f6ea651f2d2f7c87653102da4))

## v0.3.3 (2023-05-05)
### Fix
* **copier:** Simplify file comparison logic and improve logging messages ([`80017fd`](https://github.com/entelecheia/hyfi/commit/80017fd0644adcc1a6c7bf5abd7dc3f2e5239ddf))

## v0.3.2 (2023-05-05)
### Fix
* **dependencies:** Upgrade copier and install dependencies using poetry ([`7fae322`](https://github.com/entelecheia/hyfi/commit/7fae32276d9e644a9ec41d0e9fc2b6a8ec68470f))
* **lint:** Rename cpath to cached_path in excluded files. ([`e351ca2`](https://github.com/entelecheia/hyfi/commit/e351ca2c9309eb2c2848203d7569cddf3f723b63))
* Apply updated template ([`991a9d2`](https://github.com/entelecheia/hyfi/commit/991a9d2320cf5a6d28f2eec2c302ae508edfda3b))

## v0.3.1 (2023-05-05)
### Fix
* **cached-path:** Deps ([`20d7b89`](https://github.com/entelecheia/hyfi/commit/20d7b890d02f25a90ed9cc5ab20ec25207f173ff))
* **dependencies:** Add error message when cached-path or gdown are not installed ([`c8732ff`](https://github.com/entelecheia/hyfi/commit/c8732ffa6d41bd0686e6ba995ff07f7225c48ea5))

### Documentation
* Add HyFI example ([`8aca327`](https://github.com/entelecheia/hyfi/commit/8aca327fc9d38ba7532153c59e398f6427ef7975))

## v0.3.0 (2023-05-05)
### Feature
* **cli:** Implement run_copy command ([`0da557b`](https://github.com/entelecheia/hyfi/commit/0da557bbd990f40cb3c0fb2595a8c49bbd635fc4))
* **copier:** Add a feature to copy initial configs to dest ([`62ba225`](https://github.com/entelecheia/hyfi/commit/62ba2251f0926fc092a14acd04936563a273c354))

### Fix
* Replace __config_module__ with __about__.config_module ([`c1eda21`](https://github.com/entelecheia/hyfi/commit/c1eda21cacc24f5c7feb599e8400c02e4f420427))

## v0.2.20 (2023-04-26)
### Fix
* **dependencies:** Bump boto3 and botocore to latest versions ([`67d7e6b`](https://github.com/entelecheia/hyfi/commit/67d7e6bb2a3a1a439887ed1886e937e8b0e5c30c))

## v0.2.19 (2023-04-26)
### Fix
* **env:** Add AboutConfig metadata configuration ([`c265204`](https://github.com/entelecheia/hyfi/commit/c265204c56405aea93e8c246f96d3cee29103d47))

## v0.2.18 (2023-04-26)
### Fix
* **cli:** Remove unused import in HyfiConfig ([`c89361b`](https://github.com/entelecheia/hyfi/commit/c89361bba08c0fd724e091e5bdca3668923fecc0))

## v0.2.17 (2023-04-26)
### Fix
* **main:** Move "_about" from __cli__.py to main.py ([`a379ac6`](https://github.com/entelecheia/hyfi/commit/a379ac67808d4cd27fc6f0f494907c372198b789))

## v0.2.16 (2023-04-26)
### Fix
* **hyfi:** Move about printing logic to separate function ([`b89a595`](https://github.com/entelecheia/hyfi/commit/b89a5957d03252b434adb9025debe63f059ce871))

## v0.2.15 (2023-04-25)
### Fix
* Add about method to HyFI class ([`fe37759`](https://github.com/entelecheia/hyfi/commit/fe37759e2bf1613f9fe66730a5cb7db8dfa5078f))

## v0.2.14 (2023-04-25)
### Fix
* Authors name change ([`541c226`](https://github.com/entelecheia/hyfi/commit/541c226359e1cd79a002e2d54093bb87feb4af69))

## v0.2.13 (2023-04-22)
### Fix
* **config:** Update authors and license info in about config; remove project.toml file ([`41070f2`](https://github.com/entelecheia/hyfi/commit/41070f22db23aff2e38b49a48c2df8a6de99f168))

## v0.2.12 (2023-04-22)
### Fix
* **pyproject.toml:** Add version_pattern to update the version in the config file ([`59469a1`](https://github.com/entelecheia/hyfi/commit/59469a16744f1fdbf30b8a19b639c56c894cff63))

## v0.2.11 (2023-04-21)
### Fix
* **version:** Disable scm-version ([`b99319e`](https://github.com/entelecheia/hyfi/commit/b99319e69e09f6dc2c0f54404ee35cc4f486581a))

## v0.2.10 (2023-04-21)
### Fix
* **task:** Change cli module location ([`92f2d03`](https://github.com/entelecheia/hyfi/commit/92f2d034dc4ba6d07e2e0d2dac1017047d50c6f8))

## v0.2.9 (2023-04-21)
### Fix
* **cli:** Update hyfi script command ([`8b55a97`](https://github.com/entelecheia/hyfi/commit/8b55a97291b4ee79ec28ed7f1db3b3869c62e419))

## v0.2.8 (2023-04-21)
### Fix
* **version:** Add pre-commit command to make scm-version ([`99d54a4`](https://github.com/entelecheia/hyfi/commit/99d54a47cb3f37dae176658fcc8154f963aad26a))
* Add pre_commit_coomand (scm-version) ([`cb1d114`](https://github.com/entelecheia/hyfi/commit/cb1d1142153971e8e34dd0186546cdd1d4438c9e))
* Add pre_commit_coomand ([`4f9b227`](https://github.com/entelecheia/hyfi/commit/4f9b2274820e5327fe0df527e817496782cc628c))
* Version variable ([`9849ce3`](https://github.com/entelecheia/hyfi/commit/9849ce3637f8ddb587f87e1643b88cab528c4c1e))
* Version bump ([`849d165`](https://github.com/entelecheia/hyfi/commit/849d165711610b3bcd29ad1f45d0423abbbc8f35))

## v0.2.7 (2023-04-21)
### Fix
* Apply updated template ([`7b0c4b9`](https://github.com/entelecheia/hyfi/commit/7b0c4b92021134a9123c01fc2c486ba55f389d44))
* **main:** Add aliases for HyFI class ([`b42300e`](https://github.com/entelecheia/hyfi/commit/b42300e9348d76cf977eb6c380e0ff0cc7401c0c))

## v0.2.6 (2023-04-20)
### Fix
* **deps:** Update deps (gdown, matplotlib) ([`7c6d221`](https://github.com/entelecheia/hyfi/commit/7c6d2217dc363ba9165218bdb11fd3dcfea68ef7))

## v0.2.5 (2023-04-20)
### Fix
* **deps:** Update deps ([`8adf62b`](https://github.com/entelecheia/hyfi/commit/8adf62b7a795f06db0869ede5c40c57ada5f4f28))

## v0.2.4 (2023-04-10)
### Fix
* **utils:** Catch and log in load_extentions() ([`75e0c6c`](https://github.com/entelecheia/hyfi/commit/75e0c6cc5af5f106cba3bb147d513996ef2ad9d8))

## v0.2.3 (2023-04-08)
### Fix
* Update dependencies ([`8333186`](https://github.com/entelecheia/hyfi/commit/8333186c45f56e12825db154c6b631e8f8758858))

## v0.2.2 (2023-04-08)
### Fix
* Update optional dependencies in pyproject.toml ([`4f5c1a2`](https://github.com/entelecheia/hyfi/commit/4f5c1a28a172deb883a7a5d1561d943243a68632))

### Documentation
* Update badges on README ([`919c11e`](https://github.com/entelecheia/hyfi/commit/919c11e99fd48e40d35358b25de7797cb3f4bf6e))
* Update index ([`e3882fd`](https://github.com/entelecheia/hyfi/commit/e3882fd7b9ae8f82a2774e6995e29c077088fecd))

## v0.2.2-rc.5 (2023-03-01)


## v0.2.2-rc.4 (2023-03-01)


## v0.2.2-rc.3 (2023-03-01)


## v0.2.2-rc.2 (2023-03-01)


## v0.2.2-rc.1 (2023-03-01)


## v0.2.1 (2023-03-01)
### Fix
* Version var, dependencies ([`ad3596d`](https://github.com/entelecheia/hyfi/commit/ad3596dbc26e3263515da9efe6ef06ec231cff52))

## v0.2.0 (2023-03-01)
### Feature
* First draft of the package ([`ebbf6f5`](https://github.com/entelecheia/hyfi/commit/ebbf6f56ec4ff95c356f3f9211b05e1f9908a54b))

### Fix
* Linting source files ([`301ab9e`](https://github.com/entelecheia/hyfi/commit/301ab9e3752159b1bdc20ac3519b63f640fb2067))

## v0.1.1-rc.2 (2023-03-01)
### Documentation
* Update README ([`ccad7b8`](https://github.com/entelecheia/hyfi/commit/ccad7b8640cf87c8a15fee94721d81957144f0d7))

## v0.1.1-rc.1 (2023-03-01)


## v0.1.0 (2023-03-01)
### Feature
* Initial version ([`0c4cf1e`](https://github.com/entelecheia/hyfi/commit/0c4cf1e49761a27806e498e2dd8257a749207800))
