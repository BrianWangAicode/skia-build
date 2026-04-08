#! /usr/bin/env python3

import common, os, subprocess, sys

def main():
  os.chdir(os.path.join(os.path.dirname(__file__), os.pardir, 'skia'))

  build_type = common.build_type()
  machine = common.machine()
  system = common.system()
  ndk = common.ndk()  

  # 只支持 Windows 和 Linux，其他系统直接退出
  if system not in ['windows', 'linux']:
    print(f"Unsupported system: {system}. Only Windows and Linux are supported.")
    return 1

  if build_type == 'Debug':
    args = ['is_debug=true']
  else:
    args = ['is_official_build=true']

  args += [
    'target_cpu="' + machine + '"',
    'skia_use_system_expat=false',
    'skia_use_system_libjpeg_turbo=false',
    'skia_use_system_libpng=false',
    'skia_use_system_libwebp=false',
    'skia_use_system_zlib=false',
    'skia_use_sfntly=false',
    'skia_use_freetype=true',
    # 'skia_use_harfbuzz=true',
    'skia_use_system_harfbuzz=false',
    'skia_pdf_subset_harfbuzz=true',
    # 'skia_use_icu=true',
    'skia_use_system_icu=false',
    # 'skia_enable_skshaper=true',
    # 'skia_enable_svg=true',
    'skia_enable_skottie=true'
  ]

  if 'linux' == system:
    args += [
      'skia_use_system_freetype2=true',
      # 'skia_enable_gpu=true',
      # 'skia_use_gl=true',
      'extra_cflags_cc=["-frtti"]',
      'cxx="g++-9"',
    ]
  elif 'windows' == system:
    args += [
      'skia_use_system_freetype2=false',
      # 'skia_use_angle=true',
      'skia_use_direct3d=true',
      'extra_cflags=["-DSK_FONT_HOST_USE_SYSTEM_SETTINGS", "/MD"]',
    ]

  out = os.path.join('out', build_type + '-' + machine)
  gn = 'gn.exe' if 'windows' == system else 'gn'
  subprocess.check_call([os.path.join('bin', gn), 'gen', out, '--args=' + ' '.join(args)])
  ninja = 'ninja.exe' if 'windows' == system else 'ninja'
  subprocess.check_call([os.path.join('..', 'depot_tools', ninja), '-C', out, 'skia', 'modules'])

  return 0

if __name__ == '__main__':
  sys.exit(main())
