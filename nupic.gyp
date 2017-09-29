{
	'variables': {
		'library': 'static_library',
		 # 'library': 'shared_library',
	},
	'target_defaults': {
		'win_delay_load_hook': 'false',
		'msvs_settings': {
			 # This magical incantation is necessary because VC++will compile
			 # object files to same directory...even if they have the same name!
			'VCCLCompilerTool': {
				'ObjectFile': '$(IntDir)/%(RelativeDir)/',
				 # 'AdditionalOptions': ['/EHsc', '/wd4244']
				'WarningLevel': 0,
				'WholeProgramOptimization': 'false',
				'AdditionalOptions': ['/EHsc'],
				'ExceptionHandling': 1,
				 #  / EHsc
			},

		},
		'configurations': {
			'Debug': {
				'conditions': [
					['target_arch=="x64"', {
							'msvs_configuration_platform': 'x64',
						}
					],
					['1==1', {

							'defines': [
								'DEBUG',
							],
							'msvs_settings': {
								'VCCLCompilerTool': {
									 # 'WholeProgramOptimization': 'false',
									 # 'AdditionalOptions': ['/GL-', '/w'],
									 # ['/wd4244', '/wd4018', '/wd4133', '/wd4090'] # GL - was added because the forced optimization coming from node - gyp is disturbing the weird coding style from ffmpeg.
									'WarningLevel': 0,
									'WholeProgramOptimization': 'false',
									'AdditionalOptions': ['/EHsc'],
									'ExceptionHandling': 1,
									 #  / EHsc
									'RuntimeLibrary': 3,
									 # dll debug
								},
								'VCLinkerTool': {
									'GenerateDebugInformation': 'true',
									'conditions': [
										['target_arch=="x64"', {
												'TargetMachine': 17 #  / MACHINE: X64
											}
										],
									],

								}
							}

						}
					],
				],

			},
			'Release': {
				'conditions': [
					['target_arch=="x64"', {
							'msvs_configuration_platform': 'x64',
						}
					],
				],
				'msvs_settings': {
					'VCCLCompilerTool': {
						'WholeProgramOptimization': 'false',
						 # 'AdditionalOptions': ['/GL-', '/w'],
						 # ['/wd4244', '/wd4018', '/wd4133', '/wd4090'] # GL - was added because the forced optimization coming from node - gyp is disturbing the weird coding style from ffmpeg.
						'WarningLevel': 0,
						'WholeProgramOptimization': 'false',
						'AdditionalOptions': ['/EHsc'],
						'ExceptionHandling': 1,
						 #  / EHsc
						'RuntimeLibrary': 2,
						 # dll release
					},
					'VCLinkerTool': {
						'conditions': [
							['target_arch=="x64"', {
									'TargetMachine': 17 #  / MACHINE: X64
								}
							],
						],

					}
				}
			},
		},

		'conditions': [
			['OS == "win"', {
					'defines': [
						'DELAYIMP_INSECURE_WRITABLE_HOOKS'
					]
				}
			],
			['OS != "win"', {
					'defines': [
						'_LARGEFILE_SOURCE',
						'_FILE_OFFSET_BITS=64',

					],
					'cflags': [
						'-fPIC',
						'-std=c++11',
						'-fexceptions',
					],
					'cflags!': ['-fno-exceptions'],
					'cflags_cc!': ['-fno-exceptions'],
					'conditions': [
						['OS=="mac"', {
								'xcode_settings': {
									'GCC_ENABLE_CPP_EXCEPTIONS': 'YES'
								}
							}
						]
					],
					'conditions': [
						['OS=="solaris"', {
								'cflags': ['-pthreads'],
							}
						],
						['OS not in "solaris android"', {
								'cflags': ['-pthread'],
							}
						],
					],
				}
			],
			['OS=="android"', {
					'defines': [
						'ANDROID'
					],
				}
			],
		],
	},
	'targets':
	[
		{
			'target_name':'build_capnp_tool',
			'type':'none',
			'dependencies': [
				"../capnproto.module/capnproto.gyp:capnp",
				"../capnproto.module/capnproto.gyp:capnpc-c++",
				"../capnproto.module/capnproto.gyp:capnpc-capnp",
			]
		},
		{
			'target_name': 'nupic_core',
			 # 'type': '<(library)',
			 # 'type': 'shared_library',
			'type': 'static_library',
			'dependencies': [
				'build_capnp_tool',
				"../capnproto.module/capnproto.gyp:kj",
				"../capnproto.module/capnproto.gyp:libcapnp",
				"../yaml-cpp.module/yaml-cpp.gyp:yaml-cpp",
				"../apr.module/apr.gyp:apr",
				"../zlib.module/zlib.gyp:zlib",
			],
			'include_dirs': [
				"src",
				 # "external/common/share/capnproto/capnproto-c++-win32-0.5.3/capnproto-c++-0.5.3/src",
				 # "external/common/share/yaml-cpp/yaml-cpp-release-0.3.0/yaml-cpp-release-0.3.0/include",
				 # "external/common/share/apr/apr-1.6.2/include",
				 # "external/common/share/apr-util/apr-util-1.6.0/include",
				 # "external/common/share/zlib/zlib-1.2.8",
				"external/common/include",
			],
			"defines": [
				"CAPNP_LITE",
				
				"_SCL_SECURE_NO_WARNINGS",
				"NTA_INTERNAL",
				"NTA_COMPILER_MSVC"
			],
			'conditions': [
						['OS == "win"', {
							'defines':[
								"NTA_OS_WINDOWS",
							],
							'direct_dependent_settings': {
								'defines':[
									"NTA_OS_WINDOWS",
								],
							}
						},{
							'defines':[
							],
							'direct_dependent_settings': {
								'defines':[

								],
							}
						}],
					],
			'direct_dependent_settings': {
				'include_dirs': [
					"src",
					 # "external/common/share/capnproto/capnproto-c++-win32-0.5.3/capnproto-c++-0.5.3/src",
					 # "external/common/share/yaml-cpp/yaml-cpp-release-0.3.0/yaml-cpp-release-0.3.0/include",
					 # "external/common/share/apr/apr-1.6.2/include",
					 # "external/common/share/apr-util/apr-util-1.6.0/include",
					 # "external/common/share/zlib/zlib-1.2.8",
					"external/common/include",
				],
				"defines": [
					"CAPNP_LITE",
					"NTA_COMPILER_MSVC",
					"_SCL_SECURE_NO_WARNINGS",
					"NTA_INTERNAL",
				],
			},
			'rules': [
				{
					'rule_name': 'capnp-ext',
					'extension': 'capnp',
					'msvs_external_rule': 0,
					'msvs_cygwin_shell':0,
					'msvs_quote_cmd':1,
					
					'inputs': [
						
					],
					'outputs': [
						"src/nupic/proto/ArrayProto.capnp.cpp",
						"src/nupic/proto/ArrayProto.capnp.h",
						"src/nupic/proto/BitHistory.capnp.cpp",
						"src/nupic/proto/BitHistory.capnp.h",
						"src/nupic/proto/build.bat",
						"src/nupic/proto/Cell.capnp.cpp",
						"src/nupic/proto/Cell.capnp.h",
						"src/nupic/proto/Cells4.capnp.cpp",
						"src/nupic/proto/Cells4.capnp.h",
						"src/nupic/proto/ClaClassifier.capnp.cpp",
						"src/nupic/proto/ClaClassifier.capnp.h",
						"src/nupic/proto/ConnectionsProto.capnp.cpp",
						"src/nupic/proto/ConnectionsProto.capnp.h",
						"src/nupic/proto/LinkProto.capnp.cpp",
						"src/nupic/proto/LinkProto.capnp.h",
						"src/nupic/proto/Map.capnp.cpp",
						"src/nupic/proto/Map.capnp.h",
						"src/nupic/proto/NetworkProto.capnp.cpp",
						"src/nupic/proto/NetworkProto.capnp.h",
						"src/nupic/proto/PyRegionProto.capnp.cpp",
						"src/nupic/proto/PyRegionProto.capnp.h",
						"src/nupic/proto/RandomProto.capnp.cpp",
						"src/nupic/proto/RandomProto.capnp.h",
						"src/nupic/proto/RegionProto.capnp.cpp",
						"src/nupic/proto/RegionProto.capnp.h",
						"src/nupic/proto/SdrClassifier.capnp.cpp",
						"src/nupic/proto/SdrClassifier.capnp.h",
						"src/nupic/proto/Segment.capnp.cpp",
						"src/nupic/proto/Segment.capnp.h",
						"src/nupic/proto/SegmentUpdate.capnp.cpp",
						"src/nupic/proto/SegmentUpdate.capnp.h",
						"src/nupic/proto/SparseBinaryMatrixProto.capnp.cpp",
						"src/nupic/proto/SparseBinaryMatrixProto.capnp.h",
						"src/nupic/proto/SparseMatrixProto.capnp.cpp",
						"src/nupic/proto/SparseMatrixProto.capnp.h",
						"src/nupic/proto/SpatialPoolerProto.capnp.cpp",
						"src/nupic/proto/SpatialPoolerProto.capnp.h",
						"src/nupic/proto/SvmProto.capnp.cpp",
						"src/nupic/proto/SvmProto.capnp.h",
						"src/nupic/proto/TemporalMemoryProto.capnp.cpp",
						"src/nupic/proto/TemporalMemoryProto.capnp.h",
						"src/nupic/proto/TemporalMemoryV1.capnp.cpp",
						"src/nupic/proto/TemporalMemoryV1.capnp.h",
						"src/nupic/proto/TestNodeProto.capnp.cpp",
						"src/nupic/proto/TestNodeProto.capnp.h",
						"src/nupic/proto/VectorFileSensorProto.capnp.cpp",
						"src/nupic/proto/VectorFileSensorProto.capnp.h",
					],
					'conditions': [
						['OS == "win"', {
							
							'action=':[
								'python',
								"-cfrom subprocess import call;my_env={};my_env['PATH']=r'<(PRODUCT_DIR).';call(r'<(PRODUCT_DIR)capnp compile -oc++ <(RULE_INPUT_NAME) -I ../../',env=my_env,cwd=r'<(RULE_INPUT_DIRNAME)')",
							],
						},{
							'action=':[
								'python',
								"-cfrom subprocess import call;my_env={};my_env['PATH']=r'<(PRODUCT_DIR)';call(r'<(PRODUCT_DIR)/capnp compile -oc++ <(RULE_INPUT_NAME) -I ../../',shell=True,env=my_env,cwd=r'<(RULE_INPUT_DIRNAME)')",
							],
						}],
					],
					
					'message': 'Generating capnp <(RULE_INPUT_PATH)',
					#'process_outputs_as_sources': 1,
				},
			],
			'sources': [
				"src/nupic/proto/ArrayProto.capnp",
				"src/nupic/proto/BitHistory.capnp",
				"src/nupic/proto/Cell.capnp",
				"src/nupic/proto/Cells4.capnp",
				"src/nupic/proto/ClaClassifier.capnp",
				"src/nupic/proto/ConnectionsProto.capnp",
				"src/nupic/proto/LinkProto.capnp",
				"src/nupic/proto/Map.capnp",
				"src/nupic/proto/NetworkProto.capnp",
				"src/nupic/proto/PyRegionProto.capnp",
				"src/nupic/proto/RandomProto.capnp",
				"src/nupic/proto/RegionProto.capnp",
				"src/nupic/proto/SdrClassifier.capnp",
				"src/nupic/proto/Segment.capnp",
				"src/nupic/proto/SegmentUpdate.capnp",
				"src/nupic/proto/SparseBinaryMatrixProto.capnp",
				"src/nupic/proto/SparseMatrixProto.capnp",
				"src/nupic/proto/SpatialPoolerProto.capnp",
				"src/nupic/proto/SvmProto.capnp",
				"src/nupic/proto/TemporalMemoryProto.capnp",
				"src/nupic/proto/TemporalMemoryV1.capnp",
				"src/nupic/proto/TestNodeProto.capnp",
				"src/nupic/proto/VectorFileSensorProto.capnp",


				"external/common/include/csv.h",
				"external/common/include/CSV_README.md",
				"external/common/include/cycle_counter.hpp",

				"src/nupic/algorithms/Anomaly.cpp",
				"src/nupic/algorithms/Anomaly.hpp",
				"src/nupic/algorithms/ArrayBuffer.hpp",
				"src/nupic/algorithms/BitHistory.cpp",
				"src/nupic/algorithms/BitHistory.hpp",
				"src/nupic/algorithms/Cell.cpp",
				"src/nupic/algorithms/Cell.hpp",
				"src/nupic/algorithms/Cells4.cpp",
				"src/nupic/algorithms/Cells4.hpp",
				"src/nupic/algorithms/ClassifierResult.cpp",
				"src/nupic/algorithms/ClassifierResult.hpp",
				"src/nupic/algorithms/CondProbTable.cpp",
				"src/nupic/algorithms/CondProbTable.hpp",
				"src/nupic/algorithms/Connections.cpp",
				"src/nupic/algorithms/Connections.hpp",
				"src/nupic/algorithms/GaborNode.cpp",
				"src/nupic/algorithms/GaborNode.hpp",
				"src/nupic/algorithms/ImageSensorLite.cpp",
				"src/nupic/algorithms/ImageSensorLite.hpp",
				"src/nupic/algorithms/InSynapse.cpp",
				"src/nupic/algorithms/InSynapse.hpp",
				"src/nupic/algorithms/OutSynapse.cpp",
				"src/nupic/algorithms/OutSynapse.hpp",
				"src/nupic/algorithms/Scanning.hpp",
				"src/nupic/algorithms/SDRClassifier.cpp",
				"src/nupic/algorithms/SDRClassifier.hpp",
				"src/nupic/algorithms/Segment.cpp",
				"src/nupic/algorithms/Segment.hpp",
				"src/nupic/algorithms/SegmentUpdate.cpp",
				"src/nupic/algorithms/SegmentUpdate.hpp",
				"src/nupic/algorithms/SpatialPooler.cpp",
				"src/nupic/algorithms/SpatialPooler.hpp",
				"src/nupic/algorithms/Svm.cpp",
				"src/nupic/algorithms/Svm.hpp",
				"src/nupic/algorithms/SvmT.hpp",
				"src/nupic/algorithms/TemporalMemory.cpp",
				"src/nupic/algorithms/TemporalMemory.hpp",

				"src/nupic/encoders/ScalarEncoder.cpp",
				"src/nupic/encoders/ScalarEncoder.hpp",
				"src/nupic/encoders/ScalarSensor.cpp",
				"src/nupic/encoders/ScalarSensor.hpp",
				"src/nupic/engine/Collections.cpp",
				"src/nupic/engine/Input.cpp",
				"src/nupic/engine/Input.hpp",
				"src/nupic/engine/Link.cpp",
				"src/nupic/engine/Link.hpp",
				"src/nupic/engine/LinkPolicy.hpp",
				"src/nupic/engine/LinkPolicyFactory.cpp",
				"src/nupic/engine/LinkPolicyFactory.hpp",
				"src/nupic/engine/Network.cpp",
				"src/nupic/engine/Network.hpp",
				"src/nupic/engine/NuPIC.cpp",
				"src/nupic/engine/NuPIC.hpp",
				"src/nupic/engine/Output.cpp",
				"src/nupic/engine/Output.hpp",
				"src/nupic/engine/Region.cpp",
				"src/nupic/engine/Region.hpp",
				"src/nupic/engine/RegionImpl.cpp",
				"src/nupic/engine/RegionImpl.hpp",
				"src/nupic/engine/RegionImplFactory.cpp",
				"src/nupic/engine/RegionImplFactory.hpp",
				"src/nupic/engine/RegionIo.cpp",
				"src/nupic/engine/RegionParameters.cpp",
				"src/nupic/engine/RegisteredRegionImpl.hpp",
				"src/nupic/engine/Spec.cpp",
				"src/nupic/engine/Spec.hpp",
				"src/nupic/engine/TestFanIn2LinkPolicy.cpp",
				"src/nupic/engine/TestFanIn2LinkPolicy.hpp",
				"src/nupic/engine/TestNode.cpp",
				"src/nupic/engine/TestNode.hpp",
				"src/nupic/engine/UniformLinkPolicy.cpp",
				"src/nupic/engine/UniformLinkPolicy.hpp",
				"src/nupic/engine/YAMLUtils.cpp",
				"src/nupic/engine/YAMLUtils.hpp",
				"src/nupic/math/Array2D.hpp",
				"src/nupic/math/ArrayAlgo.hpp",
				"src/nupic/math/Convolution.hpp",
				"src/nupic/math/DenseMatrix.hpp",
				"src/nupic/math/Domain.hpp",
				"src/nupic/math/Erosion.hpp",
				"src/nupic/math/Functions.hpp",
				"src/nupic/math/GraphAlgorithms.hpp",
				"src/nupic/math/Index.hpp",
				"src/nupic/math/Math.hpp",
				"src/nupic/math/NearestNeighbor.hpp",
				"src/nupic/math/Rotation.hpp",
				"src/nupic/math/SegmentMatrixAdapter.hpp",
				"src/nupic/math/Set.hpp",
				"src/nupic/math/SparseBinaryMatrix.hpp",
				"src/nupic/math/SparseMatrix.hpp",
				"src/nupic/math/SparseMatrix01.hpp",
				"src/nupic/math/SparseMatrixAlgorithms.cpp",
				"src/nupic/math/SparseMatrixAlgorithms.hpp",
				"src/nupic/math/SparseMatrixConnections.cpp",
				"src/nupic/math/SparseMatrixConnections.hpp",
				"src/nupic/math/SparseRLEMatrix.hpp",
				"src/nupic/math/SparseTensor.hpp",
				"src/nupic/math/StlIo.cpp",
				"src/nupic/math/StlIo.hpp",
				"src/nupic/math/Topology.cpp",
				"src/nupic/math/Topology.hpp",
				"src/nupic/math/Types.hpp",
				"src/nupic/math/Utils.hpp",
				"src/nupic/ntypes/Array.hpp",
				"src/nupic/ntypes/ArrayBase.cpp",
				"src/nupic/ntypes/ArrayBase.hpp",
				"src/nupic/ntypes/ArrayRef.hpp",
				"src/nupic/ntypes/Buffer.cpp",
				"src/nupic/ntypes/Buffer.hpp",
				"src/nupic/ntypes/BundleIO.cpp",
				"src/nupic/ntypes/BundleIO.hpp",
				"src/nupic/ntypes/Collection.cpp",
				"src/nupic/ntypes/Collection.hpp",
				"src/nupic/ntypes/Dimensions.cpp",
				"src/nupic/ntypes/Dimensions.hpp",
				"src/nupic/ntypes/MemParser.cpp",
				"src/nupic/ntypes/MemParser.hpp",
				"src/nupic/ntypes/MemStream.hpp",
				"src/nupic/ntypes/NodeSet.hpp",
				"src/nupic/ntypes/ObjectModel.h",
				"src/nupic/ntypes/ObjectModel.hpp",
				"src/nupic/ntypes/Scalar.cpp",
				"src/nupic/ntypes/Scalar.hpp",
				"src/nupic/ntypes/Value.cpp",
				"src/nupic/ntypes/Value.hpp",
				"src/nupic/os/Directory.cpp",
				"src/nupic/os/Directory.hpp",
				"src/nupic/os/DynamicLibrary.cpp",
				"src/nupic/os/DynamicLibrary.hpp",
				"src/nupic/os/Env.cpp",
				"src/nupic/os/Env.hpp",
				"src/nupic/os/FStream.cpp",
				"src/nupic/os/FStream.hpp",
				"src/nupic/os/OS.cpp",
				"src/nupic/os/OS.hpp",
				"src/nupic/os/OSUnix.cpp",
				"src/nupic/os/OSWin.cpp",
				"src/nupic/os/Path.cpp",
				"src/nupic/os/Path.hpp",
				"src/nupic/os/Regex.cpp",
				"src/nupic/os/Regex.hpp",
				"src/nupic/os/Timer.cpp",
				"src/nupic/os/Timer.hpp",

				

				 # "src/nupic/regions/PyRegion.cpp",
				 # "src/nupic/regions/PyRegion.hpp",
				"src/nupic/regions/VectorFile.cpp",
				"src/nupic/regions/VectorFile.hpp",
				"src/nupic/regions/VectorFileEffector.cpp",
				"src/nupic/regions/VectorFileEffector.hpp",
				"src/nupic/regions/VectorFileSensor.cpp",
				"src/nupic/regions/VectorFileSensor.hpp",
				"src/nupic/types/BasicType.cpp",
				"src/nupic/types/BasicType.hpp",
				"src/nupic/types/Exception.hpp",
				"src/nupic/types/Fraction.cpp",
				"src/nupic/types/Fraction.hpp",
				"src/nupic/types/Serializable.hpp",
				"src/nupic/types/Types.h",
				"src/nupic/types/Types.hpp",
				"src/nupic/utils/ArrayProtoUtils.cpp",
				"src/nupic/utils/ArrayProtoUtils.hpp",
				"src/nupic/utils/GroupBy.hpp",
				"src/nupic/utils/Log.hpp",
				"src/nupic/utils/LoggingException.cpp",
				"src/nupic/utils/LoggingException.hpp",
				"src/nupic/utils/LogItem.cpp",
				"src/nupic/utils/LogItem.hpp",
				"src/nupic/utils/MovingAverage.cpp",
				"src/nupic/utils/MovingAverage.hpp",
				"src/nupic/utils/Random.cpp",
				"src/nupic/utils/Random.hpp",
				"src/nupic/utils/StringUtils.cpp",
				"src/nupic/utils/StringUtils.hpp",
				"src/nupic/utils/TRandom.cpp",
				"src/nupic/utils/TRandom.hpp",
				"src/nupic/utils/Watcher.cpp",
				"src/nupic/utils/Watcher.hpp",
				"src/nupic/Version.hpp.in",

				"external/README.md",
				"LICENSE.txt",
				"README.md",
				"RELEASE.md",
				"VERSION",

			],
		}, {
			'target_name': 'nupic_test',
			'type': 'executable',
			'dependencies': [
				"../capnproto.module/capnproto.gyp:libcapnp",
				"../apr.module/apr.gyp:apr",
				"nupic_core"
			],
			'include_dirs': [

			],
			'direct_dependent_settings': {
				'include_dirs': [
				],
			},
			'sources': [
				"external/common/include/gtest/gtest.h",
				"external/common/src/gtest/gtest-all.cpp",

				"src/test/integration/ConnectionsPerformanceTest.cpp",
				"src/test/integration/ConnectionsPerformanceTest.hpp",
				"src/test/integration/CppRegionTest.cpp",
				 # "src/test/integration/PyRegionTest.cpp",
				"src/test/unit/algorithms/AnomalyTest.cpp",
				"src/test/unit/algorithms/Cells4Test.cpp",
				"src/test/unit/algorithms/CondProbTableTest.cpp",
				"src/test/unit/algorithms/ConnectionsTest.cpp",
				"src/test/unit/algorithms/NearestNeighborUnitTest.cpp",
				"src/test/unit/algorithms/SDRClassifierTest.cpp",
				"src/test/unit/algorithms/SegmentTest.cpp",
				"src/test/unit/algorithms/SpatialPoolerTest.cpp",
				"src/test/unit/algorithms/SvmTest.cpp",
				"src/test/unit/algorithms/TemporalMemoryTest.cpp",
				"src/test/unit/encoders/ScalarEncoderTest.cpp",
				"src/test/unit/engine/fixtures/empty-regions.yaml",
				"src/test/unit/engine/fixtures/extra-yaml-fields.yaml",
				"src/test/unit/engine/fixtures/missing-link-fields.yaml",
				"src/test/unit/engine/fixtures/missing-region-fields.yaml",
				"src/test/unit/engine/fixtures/network.yaml",
				"src/test/unit/engine/fixtures/no-links.yaml",
				"src/test/unit/engine/fixtures/no-regions.yaml",
				"src/test/unit/engine/InputTest.cpp",
				"src/test/unit/engine/LinkTest.cpp",
				"src/test/unit/engine/NetworkTest.cpp",
				"src/test/unit/engine/UniformLinkPolicyTest.cpp",
				"src/test/unit/engine/YAMLUtilsTest.cpp",
				"src/test/unit/math/DenseTensorUnitTest.cpp",
				"src/test/unit/math/DenseTensorUnitTest.hpp",
				"src/test/unit/math/DomainUnitTest.cpp",
				"src/test/unit/math/DomainUnitTest.hpp",
				"src/test/unit/math/IndexUnitTest.cpp",
				"src/test/unit/math/IndexUnitTest.hpp",
				"src/test/unit/math/MathsTest.cpp",
				"src/test/unit/math/MathsTest.hpp",
				"src/test/unit/math/SegmentMatrixAdapterTest.cpp",
				"src/test/unit/math/SparseBinaryMatrixTest.cpp",
				"src/test/unit/math/SparseMatrix01UnitTest.cpp",
				"src/test/unit/math/SparseMatrix01UnitTest.hpp",
				"src/test/unit/math/SparseMatrixTest.cpp",
				"src/test/unit/math/SparseMatrixUnitTest.cpp",
				"src/test/unit/math/SparseMatrixUnitTest.hpp",
				"src/test/unit/math/SparseTensorUnitTest.cpp",
				"src/test/unit/math/SparseTensorUnitTest.hpp",
				"src/test/unit/math/TopologyTest.cpp",
				"src/test/unit/ntypes/ArrayTest.cpp",
				"src/test/unit/ntypes/BufferTest.cpp",
				"src/test/unit/ntypes/CollectionTest.cpp",
				"src/test/unit/ntypes/DimensionsTest.cpp",
				"src/test/unit/ntypes/MemParserTest.cpp",
				"src/test/unit/ntypes/MemStreamTest.cpp",
				"src/test/unit/ntypes/NodeSetTest.cpp",
				"src/test/unit/ntypes/ScalarTest.cpp",
				"src/test/unit/ntypes/ValueTest.cpp",
				"src/test/unit/os/DirectoryTest.cpp",
				"src/test/unit/os/EnvTest.cpp",
				"src/test/unit/os/OSTest.cpp",
				"src/test/unit/os/PathTest.cpp",
				"src/test/unit/os/RegexTest.cpp",
				"src/test/unit/os/TimerTest.cpp",
				 # "src/test/unit/py_support/PyHelpersTest.cpp",
				"src/test/unit/types/BasicTypeTest.cpp",
				"src/test/unit/types/ExceptionTest.cpp",
				"src/test/unit/types/FractionTest.cpp",
				"src/test/unit/UnitTestMain.cpp",
				"src/test/unit/utils/GroupByTest.cpp",
				"src/test/unit/utils/MovingAverageTest.cpp",
				"src/test/unit/utils/RandomPrivateOrig.c",
				"src/test/unit/utils/RandomTest.cpp",
				"src/test/unit/utils/WatcherTest.cpp",
			],
		}, {
			'target_name': 'nupic_hello',
			'type': 'executable',
			'dependencies': [
				"../capnproto.module/capnproto.gyp:libcapnp",
				"nupic_core"
			],
			'include_dirs': [

			],
			'direct_dependent_settings': {
				'include_dirs': [
				],
			},
			'sources': [
				"src/examples/algorithms/HelloSP_TP.cpp",
				"src/examples/algorithms/README.md",
			],
		}, {
			'target_name': 'nupic_prototest',
			'type': 'executable',
			'dependencies': [
				"../capnproto.module/capnproto.gyp:libcapnp",
				"nupic_core"
			],
			'include_dirs': [

			],
			'direct_dependent_settings': {
				'include_dirs': [
				],
			},
			'sources': [
				"src/examples/prototest.cpp",
			],
		}, {
			'target_name': 'nupic_regions',
			'type': 'executable',
			'dependencies': [
				"../capnproto.module/capnproto.gyp:libcapnp",
				"nupic_core"
			],
			'include_dirs': [

			],
			'direct_dependent_settings': {
				'include_dirs': [
				],
			},
			'sources': [
				"src/examples/regions/Data.csv",
				"src/examples/regions/HelloRegions.cpp",
			],
		}
	]
}

 # . / external / common / share / apr / apr.patch
 # . / external / common / share / apr / README.md
 #
 # . / external / common / share / apr / unix / apr - 1.5.2.tar.gz
 #
 #
 # . / external / common / share / apr - iconv / apr - iconv - 1.2.1.tar.gz
 # . / external / common / share / apr - iconv / README.md
 #
 #
 # . / external / common / share / apr - util / apru.patch
 # . / external / common / share / apr - util / README.md
 # . / external / common / share / apr - util / unix / apr - util - 1.5.4.tar.gz
 #
 # . / external / common / share / capnproto / capnproto - c++ - 0.5.3.tar.gz
 # . / external / common / share / capnproto / capnproto - c++ - win32 - 0.5.3.zip
 # . / external / common / share / capnproto / README.md
 #
 # . / external / common / share / yaml
 # . / external / common / share / yaml / README.md
 # . / external / common / share / yaml / yaml - 0.1.5.tar.gz
 # . / external / common / share / yaml - cpp
 # . / external / common / share / yaml - cpp / README.md
 # . / external / common / share / yaml - cpp / yaml - cpp - release - 0.3.0.tar.gz
 # . / external / common / share / zlib
 # . / external / common / share / zlib / README.md
 # . / external / common / share / zlib / zlib - 1.2.8.tar.gz
 # . / external / common / share / zlib / zlib.patch
 #
 # . / external / common / src / pcre - 8.37.tar.gz
 # . / external / common / src / swig - 3.0.2.tar.gz
