{
	'variables': {
		'platform' : '<(OS)',
		'variant'  : 'default',
		'bcm_host' : '<!(node -e "console.log(+require(\\"fs\\").existsSync(\\"/opt/vc/include/bcm_host.h\\"))")',
		'opengl_root'   : '<!(node -e "console.log(require(\'node-deps-opengl-raub\').root)")',
		'opengl_include': '<(opengl_root)/include',
		'opengl_bin'    : '<!(node -e "console.log(require(\'node-deps-opengl-raub\').bin)")',
	},
	'conditions': [
		# Replace gyp platform with node platform, blech
		['platform == "mac"', {'variables': {'platform': 'darwin'}}],
		['platform == "win"', {'variables': {'platform': 'windows'}}],
	],
	'targets': [
		{
			'target_name': 'webgl',
			'defines': [ 'VERSION=0.5.5' ],
			'sources': [
				'src/bindings.cpp',
				'src/image.cpp',
				'src/webgl.cpp',
			],
			'include_dirs': [
				"<!(node -e \"require('nan')\")",
				'<(opengl_include)',
			],
			'library_dirs': [ '<(opengl_bin)' ],
			'conditions': [
				[
					'OS=="mac"',
					{
						'libraries': ['-lGLEW','-lfreeimage','-framework OpenGL'],
						'include_dirs': ['/usr/local/include'],
						'library_dirs': ['/usr/local/lib'],
					}
				],
				[
					'OS=="linux"',
					{
						'libraries': [ '-lfreeimage','-lGLEW','-lGL' ]
					}
				],
				[
					'OS=="win"',
					{
						'libraries': [ 'FreeImage.lib', 'glfw3dll.lib', 'glew32.lib', 'opengl32.lib' ],
						'defines' : [
							'WIN32_LEAN_AND_MEAN',
							'VC_EXTRALEAN'
						],
						'msvs_version'  : '2013',
						'msvs_settings' : {
							'VCCLCompilerTool' : {
								'AdditionalOptions' : [
									'/O2','/Oy','/GL','/GF','/Gm-','/EHsc',
									'/MT','/GS','/Gy','/GR-','/Gd',
								]
							},
							'VCLinkerTool' : {
								'AdditionalOptions' : ['/OPT:REF','/OPT:ICF','/LTCG']
							},
						},
					}
				],
			],
		},
		
		{
			'target_name'  : 'copy_binary',
			'type'         : 'none',
			'dependencies' : ['webgl'],
			'copies'       : [
				{
					'destination' : '<(module_root_dir)/bin_<(platform)',
					'conditions'  : [
						[
							'OS=="linux"',
							{ 'files' : [] }
						],
						[
							'OS=="mac"',
							{ 'files' : [] }
						],
						[
							'OS=="win"',
							{ 'files' : [ '<(module_root_dir)/build/Release/webgl.node' ] },
						],
					]
				}
			],
		},
		
		{
			'target_name'  : 'remove_extras',
			'type'         : 'none',
			'dependencies' : ['copy_binary'],
			'actions'      : [{
				'action_name' : 'Build intermediates removed.',
				'inputs'      : [],
				'outputs'     : ['build'],
				'conditions'  : [
					[ 'OS=="linux"', { 'action' : [ 'rm -rf <@(_inputs)' ] } ],
					[ 'OS=="mac"'  , { 'action' : [ 'rm -rf <@(_inputs)' ] } ],
					[ 'OS=="win"'  , { 'action' : [
						'<(module_root_dir)/_del "<(module_root_dir)/build/Release/webgl.*" && ' +
						'<(module_root_dir)/_del "<(module_root_dir)/build/Release/obj/webgl/*.*'
					] } ],
				],
			}],
		},
		
	]
}
