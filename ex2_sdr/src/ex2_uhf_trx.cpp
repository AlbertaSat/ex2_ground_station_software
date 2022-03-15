/*!
 * @file ex2_uhf_trx.cpp
 * @author Steven Knudsen
 * @date 2021-03-30
 * @brief
 *
 * @details
 *
 * @copyright
 * Copyright (C) 2021 AlbertaSat
 *
 * @license
 * This software may not be modified or distributed in any form.
 * See the LICENSE file for details.
 */

#include <cstdint>
#include <iostream>

#include <boost/filesystem.hpp>
#include <boost/program_options.hpp>

using namespace std;
using namespace boost::program_options;
namespace bf = boost::filesystem;

bool process_command_line(
    int argc,
    const char** argv,
    string& errorControlName,
    string& codingRate,
    string& inputFileName,
    string& outputFileName)
{
  options_description desc("Program Usage", 1024, 512);
  try
  {
    variables_map vm;

    desc.add_options()
        ("help,h", "Command line options")
        ("version,V", "Display version information")
        ("errorControlName,e", value<string>()->required(), "Error Control name; LDPC_xxx")
        ("codingRate,c", value<string>()->required(), "Coding rate as string; RATE_N_M")
        ("inputFileName,i", value<string>()->required(), "Input file name, full path if not in same directory")
        ("outputFileName,o", value<string>()->default_value(""), "Output file name, full path if not in same directory");

    store(parse_command_line(argc, argv, desc), vm);

    if (vm.count("help"))
    {
      cout << desc << "\n";
//      cout << "Possible errorControlName names :" << endl;
//      uint16_t eFirst = static_cast<uint16_t>(ErrorCorrection::ErrorCorrectionCoding::LDPC_FIRST);
//      uint16_t eLast = static_cast<uint16_t>(ErrorCorrection::ErrorCorrectionCoding::LDPC_LAST);
//      for (uint16_t i = eFirst + 1; i < eLast; i++) {
//        cout << "\t" << ErrorCorrection::ErrorCorrectionName(static_cast<ErrorCorrection::ErrorCorrectionCoding>(i)) << endl;
//      }
//      cout << endl << "Possible codingRate names :" << endl;
//      eFirst = static_cast<uint16_t>(ErrorCorrection::CodingRate::RATE_FIRST);
//      eLast = static_cast<uint16_t>(ErrorCorrection::CodingRate::RATE_LAST);
//      for (uint16_t i = eFirst + 1; i < eLast; i++) {
//        cout << "\t" << ErrorCorrection::CodingRateName(static_cast<ErrorCorrection::CodingRate>(i)) << endl;
//      }
//      cout << endl << "Not all errorControlName and codingRate combinations are valid. " << endl;
      return false;
    }

    if (vm.count("version")) {
//      Version ver;
//
//      cout << "Version Information:" << endl;
//      cout << "    Git: " << ver.git() << endl;
//      cout << "    Str: " << ver.c_str() << endl;

      return false;
    }

    notify(vm);

    errorControlName = vm["errorControlName"].as<string>();
    codingRate = vm["codingRate"].as<string>();
    inputFileName = vm["inputFileName"].as<string>();
    outputFileName = vm["outputFileName"].as<string>();

    // bounds checking

  }
  catch(std::exception& e) {
    cerr << "Error: " << e.what() << endl;
    cerr << endl;
    cout << desc << endl;
    return false;
  }
  catch(...) {
    cerr << "Unknown error!" << endl;
    return false;
  }
  return true;
}

int main(int argc, const char *argv[]) {
  cout << "===== Ex-Alta 2 xxxxxxxxxxxx =====" << endl;

  string errorControlName;
  string codingRate;
  string inputFileName;
  string outputFileName;

  if (process_command_line(argc, argv,
      errorControlName,
      codingRate,
      inputFileName,
      outputFileName)) {

//    Configuration::instance(
//        errorControlName,
//        codingRate);

    //---------------------------------------------------------------------------
    // Assemble the APP-MAC-PHY chain
    //---------------------------------------------------------------------------

    cout << "Configuration complete. Starting encoding..." << endl;

//    xd::MAC my_MAC;
//    xd::TestApp my_APP(inputFileName, my_MAC.apduPayloadLength());
//
//    // Connect the MAC and the APP layers
//    my_MAC.setReceiveApdu(my_APP.receiveApdu());
//    my_APP.setSendApdu(my_MAC.sendApdu());
//
//    xd::DarkstarPHY my_PHY(outputFileName);
//
//    // Connect the MAC and PHY layers
//    my_MAC.setSendPpdu(my_PHY.transmitPpdu());
//    my_PHY.setReceivePpdu(my_MAC.receivePpdu());
//
//    my_APP.start();
    exit(EXIT_SUCCESS);
  }
  else {
    exit(EXIT_FAILURE);
  }
}

