unit_test_golay = executable('unit_test-golay', 'qa_golay.cpp',
    include_directories : incdir,
    dependencies: [gtest_dep],
    link_with: ExSDRTxRxlib
    )
    
test('golay', unit_test_golay,
    timeout: 30
    )
    
