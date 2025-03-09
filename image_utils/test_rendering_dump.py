import os
import random

# from sk_rendering_dump.main import DumpClient, ImageParam

from universe_client.image_client import DumpClient, ImageParam


class TestRenderingDump:
    client = None

    def setup(self):
        project = 'coronary'
        case_num = 'T20220724122545H5345c404'
        output_path = '/data/output'
        path_configs = {
            'cpr': 'cpr/$VESSEL',
            'clpr': 'straight/$VESSEL',
            'smpr': 'shortaxis/$VESSEL',
            'mpr': 'mpr/$UUID',
            'vr': 'vr/series/$SERIES',
        }

        client = DumpClient(project, case_num, path_configs=path_configs, universe_client='http://10.12.10.138:3031',
                            output_path=output_path)
        self.client = client

    def test_vr_images_coronary_allvessel(self):
        image_param_list = []
        image_type = 'vr'
        vr_image_param = ImageParam(
            type=image_type,
            data={
                "image_type": "VR",
                "show_path": "vessel.json",
                "columns": 1024,
                "rows": 1024,
                "output": "rendering/vr/new/coronary_allvessel",
                "ww": 800,
                "wl": 300,
                "orientation_marker": True,
                "color_type": "RGB",
                "angle": [
			[
				0,
				30,
				0
			],
			[
				45,
				0,
				0
			],
			[
				-30,
				0,
				0
			],
			[
				45,
				30,
				0
			],
			[
				-20,
				20,
				0
			],
			[
				-30,
				-30,
				0
			],
			[
				45,
				-30,
				0
			],
			[
				38,
				56,
				11
			],
			[
				14,
				51,
				31
			],
			[
				-18,
				32,
				52
			],
			[
				-28,
				17,
				56
			],
			[
				-40,
				2,
				58
			],
			[
				-53,
				-17,
				56
			],
			[
				-65,
				-33,
				51
			],
			[
				-84,
				-50,
				38
			],
			[
				-124,
				-57,
				9
			],
			[
				-169,
				-52,
				332
			],
			[
				160,
				-29,
				310
			],
			[
				146,
				-10,
				306
			],
			[
				133,
				8,
				305
			],
			[
				114,
				31,
				312
			],
			[
				82,
				54,
				335
			],
			[
				37,
				36,
				16
			],
			[
				41,
				21,
				14
			],
			[
				43,
				3,
				13
			],
			[
				47,
				-12,
				14
			],
			[
				52,
				-30,
				16
			],
			[
				58,
				-49,
				20
			],
			[
				70,
				-64,
				29
			],
			[
				117,
				-78,
				74
			],
			[
				-178,
				-72,
				138
			],
			[
				-149,
				-41,
				163
			],
			[
				-141,
				-17,
				167
			],
			[
				-137,
				5,
				167
			],
			[
				-132,
				24,
				166
			],
			[
				-121,
				53,
				158
			],
			[
				-100,
				70,
				139
			],
			[
				-34,
				78,
				76
			],
			[
				12,
				67,
				32
			],
			[
				98,
				-10,
				349
			],
			[
				90,
				-35,
				355
			],
			[
				0,
				0,
				0
			],
			[
				0,
				-30,
				0
			],
			[
				60,
				30,
				0
			],
			[
				170,
				15,
				0
			],
			[
				-25,
				-12,
				0
			],
			[
				111,
				41,
				0
			],
			[
				-144,
				-64,
				0
			],
			[
				141,
				61,
				109
			],
			[
				26,
				85,
				253
			],
			[
				150,
				15,
				82
			],
			[
				40,
				84,
				306
			],
			[
				155,
				-55,
				215
			],
			[
				26,
				53,
				19
			],
			[
				135,
				61,
				332
			],
			[
				-100,
				-100,
				200
			]
		],
                "mask_group": {
                    "use_mask_type": "asMask",
                    "filled_value": -1024,
                    'mask': [{
                        "path": "coronary_sega.npz",
                        "bitmap": 24576,
                        "calculationRule" : "",
				        "channel" : 0,
                        "type": "ushort",
                        "reverse_mask": "False",
                        "calculation_rule": "",
                    }],
                }},
            replace={'$SERIES': 'vr001'}
        )
        image_param_list.append(vr_image_param)
        result = self.client.dump_images(image_param_list, is_block=True)
        print(result)

    def test_vr_images_coronary_mainvessel(self):
        image_param_list = []
        image_type = 'vr'
        vr_image_param = ImageParam(
            type=image_type,
            data={
                "image_type": "VR",
                "show_path": "vessel.json",
                "columns": 1024,
                "rows": 1024,
                "output": "rendering/vr/new/coronary_with_mainvessel",
                "ww": 800,
                "wl": 300,
                "orientation_marker": True,
                "color_type": "RGB",
                "angles_order": "azimuth",
                "angle": [
			[
				0,
				30,
				0
			],
			[
				45,
				0,
				0
			],
			[
				-30,
				0,
				0
			],
			[
				45,
				30,
				0
			],
			[
				-20,
				20,
				0
			],
			[
				-30,
				-30,
				0
			],
			[
				45,
				-30,
				0
			],
			[
				38,
				56,
				11
			],
			[
				14,
				51,
				31
			],
			[
				-18,
				32,
				52
			],
			[
				-28,
				17,
				56
			],
			[
				-40,
				2,
				58
			],
			[
				-53,
				-17,
				56
			],
			[
				-65,
				-33,
				51
			],
			[
				-84,
				-50,
				38
			],
			[
				-124,
				-57,
				9
			],
			[
				-169,
				-52,
				332
			],
			[
				160,
				-29,
				310
			],
			[
				146,
				-10,
				306
			],
			[
				133,
				8,
				305
			],
			[
				114,
				31,
				312
			],
			[
				82,
				54,
				335
			],
			[
				37,
				36,
				16
			],
			[
				41,
				21,
				14
			],
			[
				43,
				3,
				13
			],
			[
				47,
				-12,
				14
			],
			[
				52,
				-30,
				16
			],
			[
				58,
				-49,
				20
			],
			[
				70,
				-64,
				29
			],
			[
				117,
				-78,
				74
			],
			[
				-178,
				-72,
				138
			],
			[
				-149,
				-41,
				163
			],
			[
				-141,
				-17,
				167
			],
			[
				-137,
				5,
				167
			],
			[
				-132,
				24,
				166
			],
			[
				-121,
				53,
				158
			],
			[
				-100,
				70,
				139
			],
			[
				-34,
				78,
				76
			],
			[
				12,
				67,
				32
			],
			[
				98,
				-10,
				349
			],
			[
				90,
				-35,
				355
			],
			[
				0,
				0,
				0
			],
			[
				0,
				-30,
				0
			],
			[
				60,
				30,
				0
			],
			[
				170,
				15,
				0
			],
			[
				-25,
				-12,
				0
			],
			[
				111,
				41,
				0
			],
			[
				-144,
				-64,
				0
			],
			[
				141,
				61,
				109
			],
			[
				26,
				85,
				253
			],
			[
				150,
				15,
				82
			],
			[
				40,
				84,
				306
			],
			[
				155,
				-55,
				215
			],
			[
				26,
				53,
				19
			],
			[
				135,
				61,
				332
			],
			[
				-100,
				-100,
				200
			]
		],
                "mask_group": {
                    "use_mask_type": "asMask",
                    "filled_value": -1024,
                    'mask': [{
                        "path": "coronary_sega.npz",
                        "bitmap": 24576,
                        "type": "uint",
                        "reverse_mask": "False",
                        "calculation_rule": "",
                    }],
                }},
            replace={'$SERIES': 'vr001'}
        )
        image_param_list.append(vr_image_param)
        result = self.client.dump_images(image_param_list, is_block=True)
        print(result)
    

    def test_vr_images_coronary_novessel(self):
        image_param_list = []
        image_type = 'vr'
        vr_image_param = ImageParam(
            type=image_type,
            data={
                "image_type": "VR",
                "show_path": "vessel.json",
                "columns": 1024,
                "rows": 1024,
                "output": "rendering/vr/new/coronary_with_myo_mainvessel",
                "ww": 800,
                "wl": 300,
                "orientation_marker": True,
                "color_type": "RGB",
                "angles_order": "azimuth",
                "angle": [
			[
				0,
				30,
				0
			],
			[
				45,
				0,
				0
			],
			[
				-30,
				0,
				0
			],
			[
				45,
				30,
				0
			],
			[
				-20,
				20,
				0
			],
			[
				-30,
				-30,
				0
			],
			[
				45,
				-30,
				0
			],
			[
				38,
				56,
				11
			],
			[
				14,
				51,
				31
			],
			[
				-18,
				32,
				52
			],
			[
				-28,
				17,
				56
			],
			[
				-40,
				2,
				58
			],
			[
				-53,
				-17,
				56
			],
			[
				-65,
				-33,
				51
			],
			[
				-84,
				-50,
				38
			],
			[
				-124,
				-57,
				9
			],
			[
				-169,
				-52,
				332
			],
			[
				160,
				-29,
				310
			],
			[
				146,
				-10,
				306
			],
			[
				133,
				8,
				305
			],
			[
				114,
				31,
				312
			],
			[
				82,
				54,
				335
			],
			[
				37,
				36,
				16
			],
			[
				41,
				21,
				14
			],
			[
				43,
				3,
				13
			],
			[
				47,
				-12,
				14
			],
			[
				52,
				-30,
				16
			],
			[
				58,
				-49,
				20
			],
			[
				70,
				-64,
				29
			],
			[
				117,
				-78,
				74
			],
			[
				-178,
				-72,
				138
			],
			[
				-149,
				-41,
				163
			],
			[
				-141,
				-17,
				167
			],
			[
				-137,
				5,
				167
			],
			[
				-132,
				24,
				166
			],
			[
				-121,
				53,
				158
			],
			[
				-100,
				70,
				139
			],
			[
				-34,
				78,
				76
			],
			[
				12,
				67,
				32
			],
			[
				98,
				-10,
				349
			],
			[
				90,
				-35,
				355
			],
			[
				0,
				0,
				0
			],
			[
				0,
				-30,
				0
			],
			[
				60,
				30,
				0
			],
			[
				170,
				15,
				0
			],
			[
				-25,
				-12,
				0
			],
			[
				111,
				41,
				0
			],
			[
				-144,
				-64,
				0
			],
			[
				141,
				61,
				109
			],
			[
				26,
				85,
				253
			],
			[
				150,
				15,
				82
			],
			[
				40,
				84,
				306
			],
			[
				155,
				-55,
				215
			],
			[
				26,
				53,
				19
			],
			[
				135,
				61,
				332
			],
			[
				-100,
				-100,
				200
			]
		],
                "mask_group": {
                    "use_mask_type": "asMask",
                    "filled_value": -1024,
                    'mask': [{
                            "bitmap" : 24576,
                            "calculationRule" : "",
                            "channel" : 0,
                            "path" : "coronary_sega.npz",
                            "reverseMask" : False,
                            "type" : "uint"
                        },
                        {
                            "bitmap" : 4628,
                            "calculationRule" : "add",
                            "channel" : 0,
                            "path" : "coronary_sega.npz",
                            "reverseMask" : False,
                            "type" : "uint"
                        }],
                }},
            replace={'$SERIES': 'vr001'}
        )
        image_param_list.append(vr_image_param)
        result = self.client.dump_images(image_param_list, is_block=True)
        print(result)

    def test_vr_images_coronary_with_myo_allvessel(self):
        image_param_list = []
        image_type = 'VR'
        vr_image_param = ImageParam(
            type=image_type,
            data={
                "image_type": "userconfig",
                "show_path": "vessel.json",
                "columns": 1024,
                "rows": 1024,
                "output": "rendering/vr/new/coronary_with_myo_novessel",
                "ww": 800,
                "wl": 300,
                "orientation_marker": True,
                "color_type": "RGB",
                "angle": [
			[
				0,
				30,
				0
			],
			[
				45,
				0,
				0
			],
			[
				-30,
				0,
				0
			],
			[
				45,
				30,
				0
			],
			[
				-20,
				20,
				0
			],
			[
				-30,
				-30,
				0
			],
			[
				45,
				-30,
				0
			],
			[
				38,
				56,
				11
			],
			[
				14,
				51,
				31
			],
			[
				-18,
				32,
				52
			],
			[
				-28,
				17,
				56
			],
			[
				-40,
				2,
				58
			],
			[
				-53,
				-17,
				56
			],
			[
				-65,
				-33,
				51
			],
			[
				-84,
				-50,
				38
			],
			[
				-124,
				-57,
				9
			],
			[
				-169,
				-52,
				332
			],
			[
				160,
				-29,
				310
			],
			[
				146,
				-10,
				306
			],
			[
				133,
				8,
				305
			],
			[
				114,
				31,
				312
			],
			[
				82,
				54,
				335
			],
			[
				37,
				36,
				16
			],
			[
				41,
				21,
				14
			],
			[
				43,
				3,
				13
			],
			[
				47,
				-12,
				14
			],
			[
				52,
				-30,
				16
			],
			[
				58,
				-49,
				20
			],
			[
				70,
				-64,
				29
			],
			[
				117,
				-78,
				74
			],
			[
				-178,
				-72,
				138
			],
			[
				-149,
				-41,
				163
			],
			[
				-141,
				-17,
				167
			],
			[
				-137,
				5,
				167
			],
			[
				-132,
				24,
				166
			],
			[
				-121,
				53,
				158
			],
			[
				-100,
				70,
				139
			],
			[
				-34,
				78,
				76
			],
			[
				12,
				67,
				32
			],
			[
				98,
				-10,
				349
			],
			[
				90,
				-35,
				355
			],
			[
				0,
				0,
				0
			],
			[
				0,
				-30,
				0
			],
			[
				60,
				30,
				0
			],
			[
				170,
				15,
				0
			],
			[
				-25,
				-12,
				0
			],
			[
				111,
				41,
				0
			],
			[
				-144,
				-64,
				0
			],
			[
				141,
				61,
				109
			],
			[
				26,
				85,
				253
			],
			[
				150,
				15,
				82
			],
			[
				40,
				84,
				306
			],
			[
				155,
				-55,
				215
			],
			[
				26,
				53,
				19
			],
			[
				135,
				61,
				332
			],
			[
				-100,
				-100,
				200
			]
		],
                "mask_group": {
                    "use_mask_type": "asMask",
                    "filled_value": -1,
                    'mask': [{
                        "path": "coronary_sega.npz",
                        "bitmap": 24576,
                        "type": "ushort",
                        "reverse_mask": "False",
                        "calculation_rule": "",
                    }],
                }},
            replace={'$SERIES': 'vr001'}
        )
        image_param_list.append(vr_image_param)
        result = self.client.dump_images(image_param_list, is_block=True)
        print(result)

    def test_vr_images_coronary_with_myo_mainvessel(self):
        image_param_list = []
        image_type = 'vr'
        vr_image_param = ImageParam(
            type=image_type,
            data={
                "image_type": "VR",
                "show_path": "vessel.json",
                "columns": 1024,
                "rows": 1024,
                "output": "rendering/vr/new/coronary_with_myo_mainvessel",
                "ww": 800,
                "wl": 300,
                "orientation_marker": True,
                "color_type": "RGB",
                "angles_order": "azimuth",
                "angle": [
			[
				0,
				30,
				0
			],
			[
				45,
				0,
				0
			],
			[
				-30,
				0,
				0
			],
			[
				45,
				30,
				0
			],
			[
				-20,
				20,
				0
			],
			[
				-30,
				-30,
				0
			],
			[
				45,
				-30,
				0
			],
			[
				38,
				56,
				11
			],
			[
				14,
				51,
				31
			],
			[
				-18,
				32,
				52
			],
			[
				-28,
				17,
				56
			],
			[
				-40,
				2,
				58
			],
			[
				-53,
				-17,
				56
			],
			[
				-65,
				-33,
				51
			],
			[
				-84,
				-50,
				38
			],
			[
				-124,
				-57,
				9
			],
			[
				-169,
				-52,
				332
			],
			[
				160,
				-29,
				310
			],
			[
				146,
				-10,
				306
			],
			[
				133,
				8,
				305
			],
			[
				114,
				31,
				312
			],
			[
				82,
				54,
				335
			],
			[
				37,
				36,
				16
			],
			[
				41,
				21,
				14
			],
			[
				43,
				3,
				13
			],
			[
				47,
				-12,
				14
			],
			[
				52,
				-30,
				16
			],
			[
				58,
				-49,
				20
			],
			[
				70,
				-64,
				29
			],
			[
				117,
				-78,
				74
			],
			[
				-178,
				-72,
				138
			],
			[
				-149,
				-41,
				163
			],
			[
				-141,
				-17,
				167
			],
			[
				-137,
				5,
				167
			],
			[
				-132,
				24,
				166
			],
			[
				-121,
				53,
				158
			],
			[
				-100,
				70,
				139
			],
			[
				-34,
				78,
				76
			],
			[
				12,
				67,
				32
			],
			[
				98,
				-10,
				349
			],
			[
				90,
				-35,
				355
			],
			[
				0,
				0,
				0
			],
			[
				0,
				-30,
				0
			],
			[
				60,
				30,
				0
			],
			[
				170,
				15,
				0
			],
			[
				-25,
				-12,
				0
			],
			[
				111,
				41,
				0
			],
			[
				-144,
				-64,
				0
			],
			[
				141,
				61,
				109
			],
			[
				26,
				85,
				253
			],
			[
				150,
				15,
				82
			],
			[
				40,
				84,
				306
			],
			[
				155,
				-55,
				215
			],
			[
				26,
				53,
				19
			],
			[
				135,
				61,
				332
			],
			[
				-100,
				-100,
				200
			]
		],
                "mask_group": {
                    "use_mask_type": "asMask",
                    "filled_value": -1,
                    'mask': [{
                            "bitmap" : 24576,
                            "calculationRule" : "",
                            "channel" : 0,
                            "path" : "coronary_sega.npz",
                            "reverseMask" : False,
                            "type" : "uint"
                        },
                        {
                            "bitmap" : 4628,
                            "calculationRule" : "add",
                            "channel" : 0,
                            "path" : "coronary_sega.npz",
                            "reverseMask" : False,
                            "type" : "uint"
                        }],
                }},
            replace={'$SERIES': 'vr001'}
        )
        image_param_list.append(vr_image_param)
        result = self.client.dump_images(image_param_list, is_block=True)
        print(result)

    def test_vr_images_coronary_with_myo_novessel(self):
        image_param_list = []
        image_type = 'vr'
        vr_image_param = ImageParam(
            type=image_type,
            data={
                "image_type": "VR",
                "show_path": "vessel.json",
                "columns": 1024,
                "rows": 1024,
                "output": "rendering/vr/new/coronary_with_myo_novessel",
                "ww": 800,
                "wl": 300,
                "orientation_marker": True,
                "color_type": "RGB",
                "angles_order": "azimuth",
                "angle": [
			[
				0,
				30,
				0
			],
			[
				45,
				0,
				0
			],
			[
				-30,
				0,
				0
			],
			[
				45,
				30,
				0
			],
			[
				-20,
				20,
				0
			],
			[
				-30,
				-30,
				0
			],
			[
				45,
				-30,
				0
			],
			[
				38,
				56,
				11
			],
			[
				14,
				51,
				31
			],
			[
				-18,
				32,
				52
			],
			[
				-28,
				17,
				56
			],
			[
				-40,
				2,
				58
			],
			[
				-53,
				-17,
				56
			],
			[
				-65,
				-33,
				51
			],
			[
				-84,
				-50,
				38
			],
			[
				-124,
				-57,
				9
			],
			[
				-169,
				-52,
				332
			],
			[
				160,
				-29,
				310
			],
			[
				146,
				-10,
				306
			],
			[
				133,
				8,
				305
			],
			[
				114,
				31,
				312
			],
			[
				82,
				54,
				335
			],
			[
				37,
				36,
				16
			],
			[
				41,
				21,
				14
			],
			[
				43,
				3,
				13
			],
			[
				47,
				-12,
				14
			],
			[
				52,
				-30,
				16
			],
			[
				58,
				-49,
				20
			],
			[
				70,
				-64,
				29
			],
			[
				117,
				-78,
				74
			],
			[
				-178,
				-72,
				138
			],
			[
				-149,
				-41,
				163
			],
			[
				-141,
				-17,
				167
			],
			[
				-137,
				5,
				167
			],
			[
				-132,
				24,
				166
			],
			[
				-121,
				53,
				158
			],
			[
				-100,
				70,
				139
			],
			[
				-34,
				78,
				76
			],
			[
				12,
				67,
				32
			],
			[
				98,
				-10,
				349
			],
			[
				90,
				-35,
				355
			],
			[
				0,
				0,
				0
			],
			[
				0,
				-30,
				0
			],
			[
				60,
				30,
				0
			],
			[
				170,
				15,
				0
			],
			[
				-25,
				-12,
				0
			],
			[
				111,
				41,
				0
			],
			[
				-144,
				-64,
				0
			],
			[
				141,
				61,
				109
			],
			[
				26,
				85,
				253
			],
			[
				150,
				15,
				82
			],
			[
				40,
				84,
				306
			],
			[
				155,
				-55,
				215
			],
			[
				26,
				53,
				19
			],
			[
				135,
				61,
				332
			],
			[
				-100,
				-100,
				200
			]
		],
                "mask_group": {
                    "use_mask_type": "asMask",
                    "filled_value": -1,
                    'mask': [{
				"bitmap" : 24576,
				"calculationRule" : "",
				"channel" : 0,
				"path" : "coronary_sega.npz",
				"reverseMask" : False,
				"type" : "uint"
			},
			{
				"bitmap" : 4628,
				"calculationRule" : "add",
				"channel" : 0,
				"path" : "coronary_sega.npz",
				"reverseMask" : False,
				"type" : "uint"
			}],
                }},
            replace={'$SERIES': 'vr001'}
        )
        image_param_list.append(vr_image_param)
        result = self.client.dump_images(image_param_list, is_block=True)
        print(result)


    def test_vr_images_coronary_mip(self):
        image_param_list = []
        image_type = 'VR'
        vr_image_param = ImageParam(

            type=image_type,
            data={
                "image_type": "maxmip",
                "show_path": "vessel.json",
                "columns": 1024,
                "rows": 1024,
                "output": "rendering/vr/new/mip_",
                "ww": 800,
                "wl": 300,
                "orientation_marker": True,
                "color_type": "RGB",
                "angles_order": "azimuth",
                "angle": [
			[
				0,
				30,
				0
			],
			[
				45,
				0,
				0
			],
			[
				-30,
				0,
				0
			],
			[
				45,
				30,
				0
			],
			[
				-20,
				20,
				0
			],
			[
				-30,
				-30,
				0
			],
			[
				45,
				-30,
				0
			],
			[
				38,
				56,
				11
			],
			[
				14,
				51,
				31
			],
			[
				-18,
				32,
				52
			],
			[
				-28,
				17,
				56
			],
			[
				-40,
				2,
				58
			],
			[
				-53,
				-17,
				56
			],
			[
				-65,
				-33,
				51
			],
			[
				-84,
				-50,
				38
			],
			[
				-124,
				-57,
				9
			],
			[
				-169,
				-52,
				332
			],
			[
				160,
				-29,
				310
			],
			[
				146,
				-10,
				306
			],
			[
				133,
				8,
				305
			],
			[
				114,
				31,
				312
			],
			[
				82,
				54,
				335
			],
			[
				37,
				36,
				16
			],
			[
				41,
				21,
				14
			],
			[
				43,
				3,
				13
			],
			[
				47,
				-12,
				14
			],
			[
				52,
				-30,
				16
			],
			[
				58,
				-49,
				20
			],
			[
				70,
				-64,
				29
			],
			[
				117,
				-78,
				74
			],
			[
				-178,
				-72,
				138
			],
			[
				-149,
				-41,
				163
			],
			[
				-141,
				-17,
				167
			],
			[
				-137,
				5,
				167
			],
			[
				-132,
				24,
				166
			],
			[
				-121,
				53,
				158
			],
			[
				-100,
				70,
				139
			],
			[
				-34,
				78,
				76
			],
			[
				12,
				67,
				32
			],
			[
				98,
				-10,
				349
			],
			[
				90,
				-35,
				355
			],
			[
				0,
				0,
				0
			],
			[
				0,
				-30,
				0
			],
			[
				60,
				30,
				0
			],
			[
				170,
				15,
				0
			],
			[
				-25,
				-12,
				0
			],
			[
				111,
				41,
				0
			],
			[
				-144,
				-64,
				0
			],
			[
				141,
				61,
				109
			],
			[
				26,
				85,
				253
			],
			[
				150,
				15,
				82
			],
			[
				40,
				84,
				306
			],
			[
				155,
				-55,
				215
			],
			[
				26,
				53,
				19
			],
			[
				135,
				61,
				332
			],
			[
				-100,
				-100,
				200
			]
		],
                "mask_group": {
                    "use_mask_type": "asMask",
                    "filled_value": -1024,
                    'mask': [{
                        "bitmap" : 24576,
                        "calculationRule" : "",
                        "channel" : 0,
                        "path" : "coronary_sega.npz",
                        "reverseMask" : False,
                        "type" : "uint"
                    }],
                }},
            replace={'$SERIES': 'vr001'}
        )
        image_param_list.append(vr_image_param)
        result = self.client.dump_images(image_param_list, is_block=True)
        print(result)

    def test_vr_images_coronary_invert_mip(self):
        image_param_list = []
        image_type = 'VR'
        vr_image_param = ImageParam(
            type=image_type,
            data={
                "image_type": "invmaxmip",
                "show_path": "vessel.json",
                "columns": 1024,
                "rows": 1024,
                "output": "rendering/vr/new/invmaxmip",
                "ww": 800,
                "wl": 244,
                "orientation_marker": True,
                "color_type": "RGB",
                "angles_order": "azimuth",
                "angle": [
			[
				0,
				30,
				0
			],
			[
				45,
				0,
				0
			],
			[
				-30,
				0,
				0
			],
			[
				45,
				30,
				0
			],
			[
				-20,
				20,
				0
			],
			[
				-30,
				-30,
				0
			],
			[
				45,
				-30,
				0
			],
			[
				38,
				56,
				11
			],
			[
				14,
				51,
				31
			],
			[
				-18,
				32,
				52
			],
			[
				-28,
				17,
				56
			],
			[
				-40,
				2,
				58
			],
			[
				-53,
				-17,
				56
			],
			[
				-65,
				-33,
				51
			],
			[
				-84,
				-50,
				38
			],
			[
				-124,
				-57,
				9
			],
			[
				-169,
				-52,
				332
			],
			[
				160,
				-29,
				310
			],
			[
				146,
				-10,
				306
			],
			[
				133,
				8,
				305
			],
			[
				114,
				31,
				312
			],
			[
				82,
				54,
				335
			],
			[
				37,
				36,
				16
			],
			[
				41,
				21,
				14
			],
			[
				43,
				3,
				13
			],
			[
				47,
				-12,
				14
			],
			[
				52,
				-30,
				16
			],
			[
				58,
				-49,
				20
			],
			[
				70,
				-64,
				29
			],
			[
				117,
				-78,
				74
			],
			[
				-178,
				-72,
				138
			],
			[
				-149,
				-41,
				163
			],
			[
				-141,
				-17,
				167
			],
			[
				-137,
				5,
				167
			],
			[
				-132,
				24,
				166
			],
			[
				-121,
				53,
				158
			],
			[
				-100,
				70,
				139
			],
			[
				-34,
				78,
				76
			],
			[
				12,
				67,
				32
			],
			[
				98,
				-10,
				349
			],
			[
				90,
				-35,
				355
			],
			[
				0,
				0,
				0
			],
			[
				0,
				-30,
				0
			],
			[
				60,
				30,
				0
			],
			[
				170,
				15,
				0
			],
			[
				-25,
				-12,
				0
			],
			[
				111,
				41,
				0
			],
			[
				-144,
				-64,
				0
			],
			[
				141,
				61,
				109
			],
			[
				26,
				85,
				253
			],
			[
				150,
				15,
				82
			],
			[
				40,
				84,
				306
			],
			[
				155,
				-55,
				215
			],
			[
				26,
				53,
				19
			],
			[
				135,
				61,
				332
			],
			[
				-100,
				-100,
				200
			]
		],
                "mask_group": {
                    "use_mask_type": "asMask",
                    "filled_value": -1024,
                    'mask': [{
                        "bitmap" : 24576,
                        "calculationRule" : "",
                        "channel" : 0,
                        "path" : "coronary_sega.npz",
                        "reverseMask" : False,
                        "type" : "uint"
                    }],
                }},
            replace={'$SERIES': 'vr001'}
        )
        image_param_list.append(vr_image_param)
        result = self.client.dump_images(image_param_list, is_block=True)
        print(result)

    def test_vr_images_coronary_dsa(self):
        image_param_list = []
        image_type = 'vr'
        vr_image_param = ImageParam(
            type=image_type,
            data={
                "image_type": "dsa",
                "show_path": "vessel.json",
                "columns": 1024,
                "rows": 1024,
                "output": "rendering/vr/new/dsa",
                "ww": 255,
                "wl": 127,
                "orientation_marker": True,
                "color_type": "RGB",
                "angles_order": "azimuth",
                "angle": [
			[
				0,
				30,
				0
			],
			[
				45,
				0,
				0
			],
			[
				-30,
				0,
				0
			],
			[
				45,
				30,
				0
			],
			[
				-20,
				20,
				0
			],
			[
				-30,
				-30,
				0
			],
			[
				45,
				-30,
				0
			],
			[
				38,
				56,
				11
			],
			[
				14,
				51,
				31
			],
			[
				-18,
				32,
				52
			],
			[
				-28,
				17,
				56
			],
			[
				-40,
				2,
				58
			],
			[
				-53,
				-17,
				56
			],
			[
				-65,
				-33,
				51
			],
			[
				-84,
				-50,
				38
			],
			[
				-124,
				-57,
				9
			],
			[
				-169,
				-52,
				332
			],
			[
				160,
				-29,
				310
			],
			[
				146,
				-10,
				306
			],
			[
				133,
				8,
				305
			],
			[
				114,
				31,
				312
			],
			[
				82,
				54,
				335
			],
			[
				37,
				36,
				16
			],
			[
				41,
				21,
				14
			],
			[
				43,
				3,
				13
			],
			[
				47,
				-12,
				14
			],
			[
				52,
				-30,
				16
			],
			[
				58,
				-49,
				20
			],
			[
				70,
				-64,
				29
			],
			[
				117,
				-78,
				74
			],
			[
				-178,
				-72,
				138
			],
			[
				-149,
				-41,
				163
			],
			[
				-141,
				-17,
				167
			],
			[
				-137,
				5,
				167
			],
			[
				-132,
				24,
				166
			],
			[
				-121,
				53,
				158
			],
			[
				-100,
				70,
				139
			],
			[
				-34,
				78,
				76
			],
			[
				12,
				67,
				32
			],
			[
				98,
				-10,
				349
			],
			[
				90,
				-35,
				355
			],
			[
				0,
				0,
				0
			],
			[
				0,
				-30,
				0
			],
			[
				60,
				30,
				0
			],
			[
				170,
				15,
				0
			],
			[
				-25,
				-12,
				0
			],
			[
				111,
				41,
				0
			],
			[
				-144,
				-64,
				0
			],
			[
				141,
				61,
				109
			],
			[
				26,
				85,
				253
			],
			[
				150,
				15,
				82
			],
			[
				40,
				84,
				306
			],
			[
				155,
				-55,
				215
			],
			[
				26,
				53,
				19
			],
			[
				135,
				61,
				332
			],
			[
				-100,
				-100,
				200
			]
		],
                "mask_group": {
                    "use_mask_type": "asVolume",
                    "filled_value": -1,
                    'mask': [{
                        "bitmap" : 24576,
                        "calculationRule" : "",
                        "channel" : 0,
                        "path" : "coronary_sega.npz",
                        "reverseMask" : False,
                        "type" : "uint"
                    }],
                }},
            replace={'$SERIES': 'vr001'}
        )
        image_param_list.append(vr_image_param)
        result = self.client.dump_images(image_param_list, is_block=True)
        print(result)