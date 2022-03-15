project('ex2_uhf_trx', 'c', 'cpp',
    license: 'proprietary',
    version: '0.5.0',
    default_options : [
#        'c_args=pr', 'cpp_args=pr',
#        'c_std=c89', 'cpp_std=c++14',
#        'cpp_std=c++14',
        'warning_level=3',
        'buildtype=release',
#        'werror=true',
        ],
    )

add_project_arguments(
    language: 'c,cpp')

cpp = meson.get_compiler('cpp')

home = run_command('sh', '-c', 'echo $HOME')
HOME_DIR = home.stdout().strip()
message('home = ' + HOME_DIR)

boost_dep = dependency('boost', modules: [
        'program_options',
        'iostreams',
        'filesystem',
        'system',
        'thread'
        ],
    )

glog_dep = dependency('libglog')
eigen_dep = dependency('eigen3')
#liquid_dep = dependency('liquid', required: false)

#if not liquid_dep.found()
#    foreach incdir: ['/usr/include/liquid', '/usr/local/include/liquid']
#        if cpp.has_header('liquid.h', args: '-I' + incdir)
#            liquid_inc = include_directories(incdir)
#            break
#        endif
#    endforeach
#
#    liquid_dep = declare_dependency(
#        dependencies: cpp.find_library('liquid'),
#        include_directories: liquid_inc,
#        )
#endif

#if not liquid_dep.found()
#    error('unable to find dependency')
#endif

thread_dep = dependency('threads')

freertos_incdir = include_directories(
    'include',
    HOME_DIR / 'Development/FreeRTOS/Source/include',
    HOME_DIR / 'Development/FreeRTOS/Source/portable/ThirdParty/GCC/Posix',
    HOME_DIR / 'Development/FreeRTOS/Source/portable/ThirdParty/GCC/Posix/utils',
    HOME_DIR / 'Development/FreeRTOS/Demo/Common/include',
    HOME_DIR / 'Development/FreeRTOS-Plus/Source/FreeRTOS-Plus-Trace/Include'
    )
    
local_source = [
    'src/console.c',
    'src/main_blinky.c',
    'src/main.c',
    ]
    
freertos_source = [
    HOME_DIR / 'Development/FreeRTOS/Source/croutine.c',
    HOME_DIR / 'Development/FreeRTOS/Source/event_groups.c',
    HOME_DIR / 'Development/FreeRTOS/Source/list.c',
    HOME_DIR / 'Development/FreeRTOS/Source/queue.c',
    HOME_DIR / 'Development/FreeRTOS/Source/stream_buffer.c',
    HOME_DIR / 'Development/FreeRTOS/Source/tasks.c',
    HOME_DIR / 'Development/FreeRTOS/Source/timers.c',
# Memory manager (use malloc() / free() )
    HOME_DIR / 'Development/FreeRTOS/Source/portable/MemMang/heap_3.c',
# posix port
    HOME_DIR / 'Development/FreeRTOS/Source/portable/ThirdParty/GCC/Posix/utils/wait_for_event.c',
    HOME_DIR / 'Development/FreeRTOS/Source/portable/ThirdParty/GCC/Posix/port.c'
]

core_source_files = [
#    'lib/app_layer/app.cpp',
#    'lib/configuration/configuration.cpp',
#    'lib/error_control/crc.cpp',
#    'lib/error_control/interleaver.cpp',
#    'lib/error_control/scrambler.cpp',
    'lib/error_control/error_correction.cpp',
    'lib/error_control/golay.cpp',
#    'lib/math/gf2poly.cpp',
#    'lib/math/galoisLFSR.cpp',
##    'lib/pdu/pdu.cpp',
##    'lib/mac_layer/mac.cpp',
#    'lib/mac_layer/mac_high.cpp',
#    'lib/mac_layer/mac_low.cpp',
#    'lib/mac_layer/pdu/mpdu.cpp',
    'lib/mac_layer/pdu/mpduHeader.cpp',
#    'lib/phy_layer/mls.cpp',
#    'lib/utilities/version.cpp',
#    'lib/utilities/vectorTools.cpp',
#    'lib/error_control/qcldpc/ldpc.cpp',
#    'lib/error_control/qcldpc/parity_check.cpp',
#    'lib/app_layer/pdu/apdu.cpp',
#    'lib/math/eigen/matrix2d.cpp',
##    'lib/phy_layer/modulation.cpp',
##    'lib/phy_layer/phy.cpp',
##    'lib/phy_layer/pdu/ppdu_cf.cpp',
##    'lib/phy_layer/pdu/ppdu_f.cpp',
##    'lib/phy_layer/pdu/ppdu_u8.cpp',
##    'lib/phy_layer/pdu/ppdu_u32.cpp',
    ]

applyChannel_files = [
#    'lib/channel/ChannelRxPower.cpp',
#    'lib/math/galoisLFSR.cpp',
#    'lib/pdu/pdu.cpp',
#    'lib/phy_layer/pdu/ppdu_u8.cpp',
    ]

incdir = include_directories(
    '/usr/local/include/csp',
    'include/HAL',
#    'include/app_layer',
#    'include/app_layer/pdu',
#    'include/channel',
#    'include/configuration',
    'include/error_control',
#    'include/error_control/qcldpc',
    'include/mac_layer',
    'include/mac_layer/pdu',
#    'include/math',
#    'include/math/eigen',
    'include/pdu',
    'include/phy_layer',
    'include/phy_layer/pdu',
#    'include/utilities',
    'include',
    )

ExSDRTxRxlib = library('exsdrlib',
    sources: core_source_files,
    include_directories: [incdir, freertos_incdir],
#    dependencies: boost_dep,
    version: meson.project_version(),
    soversion: 0,
    install: true,
    )

#ApplyChannellib = library('dstransceiverchannel',
#    sources: applyChannel_files,
#    include_directories: incdir,
#    dependencies: boost_dep,
#    version: meson.project_version(),
#    soversion: 0,
#    install: true,
#    )

executable('ex2_uhf_trx', 'src/ex2_uhf_trx.cpp',
    include_directories: incdir,
    dependencies: boost_dep,
    link_with: ExSDRTxRxlib,
    install: true,
    )

#freertoslib = library('rtoslib',
#    sources: freertos_source, demo_source, trace_source,
#    include_directories: freertos_incdir,
#    dependencies: boost_dep,
#    version: meson.project_version(),
#    soversion: 0,
#    install: true,
#    )
            
executable('FreeRTOS_tut', local_source, freertos_source,
    include_directories: freertos_incdir,
    dependencies: thread_dep,
#    link_with: [freertoslib, demolib, tracelib],
    install: true,
    )
    


#install_subdir('lib/error_control/qcldpc/fec/ldpc/802.11/proto_H/',
#    install_dir: '/opt/darkstar/fec/ldpc/802.11/'
#    )

gtest_dep = dependency('gtest_main', required: false)
if gtest_dep.found()
    subdir('unit_tests')
endif

#subdir('Documentation')
