<!--next-version-placeholder-->

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
