//
// KIM-API: An API for interatomic models
// Copyright (c) 2013--2022, Regents of the University of Minnesota.
// All rights reserved.
//
// Contributors:
//    Ryan S. Elliott
//
// SPDX-License-Identifier: LGPL-2.1-or-later
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or (at your option) any later version.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with this library; if not, write to the Free Software Foundation,
// Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
//

//
// Release: This file is part of the kim-api-2.3.0 package.
//


#include <cstddef>

#ifndef KIM_FUNCTION_TYPES_HPP_
#include "KIM_FunctionTypes.hpp"
#endif

extern "C" {
#ifndef KIM_FUNCTION_TYPES_H_
#include "KIM_FunctionTypes.h"  // IWYU pragma: keep
#endif
}

#ifndef KIM_LANGUAGE_NAME_HPP_
#include "KIM_LanguageName.hpp"
#endif

#ifndef KIM_COLLECTION_ITEM_TYPE_HPP_
#include "KIM_CollectionItemType.hpp"
#endif

#ifndef KIM_SHARED_LIBRARY_SCHEMA_HPP_
#include "KIM_SharedLibrarySchema.hpp"
#endif


using namespace KIM::SHARED_LIBRARY_SCHEMA;

extern "C" {
// clang-format off
int kim_shared_library_schema_version = 2;

KIM::ModelCreateFunction model_create;



extern unsigned int const item_compiled_with_version_txt_len;
extern unsigned char const item_compiled_with_version_txt[];
extern unsigned int const kimspec_edn_len;
extern unsigned char const kimspec_edn[];



static SharedLibrarySchemaV2::EmbeddedFile const METADATA_FILE_Files[] = {
  {"item-compiled-with-version.txt", item_compiled_with_version_txt_len, item_compiled_with_version_txt},
  {"kimspec.edn", kimspec_edn_len, kimspec_edn}
};

SharedLibrarySchemaV2 kim_shared_library_schema = {
    KIM::COLLECTION_ITEM_TYPE::portableModel,  // Item Type
    "KUSP__MO_000000000000_000",  // Item Name
    KIM::LANGUAGE_NAME::cpp,  // Create Routine Language
    reinterpret_cast<KIM::Function *>(model_create),  // Create Routine Name
    NULL,  // Item Driver Name
    NULL,  // smspec File
    0,  // Number of Parameter Files
    NULL,  // Embedded Parameter Files
    2,  // Number of Metadata Files
    METADATA_FILE_Files  // Embedded Metadata Files
};
}
// clang-format on
