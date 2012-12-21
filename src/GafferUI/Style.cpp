//////////////////////////////////////////////////////////////////////////
//  
//  Copyright (c) 2011, John Haddon. All rights reserved.
//  Copyright (c) 2012, Image Engine Design Inc. All rights reserved.
//  
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met:
//  
//      * Redistributions of source code must retain the above
//        copyright notice, this list of conditions and the following
//        disclaimer.
//  
//      * Redistributions in binary form must reproduce the above
//        copyright notice, this list of conditions and the following
//        disclaimer in the documentation and/or other materials provided with
//        the distribution.
//  
//      * Neither the name of John Haddon nor the names of
//        any other contributors to this software may be used to endorse or
//        promote products derived from this software without specific prior
//        written permission.
//  
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
//  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
//  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
//  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
//  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
//  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
//  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//  
//////////////////////////////////////////////////////////////////////////

#include "GafferUI/Style.h"
#include "GafferUI/StandardStyle.h"

#include "IECore/Exception.h"
#include "IECore/SimpleTypedData.h"

using namespace GafferUI;

IE_CORE_DEFINERUNTIMETYPED( Style );

StylePtr Style::g_defaultStyle = new StandardStyle;

Style::Style()
{
}

Style::~Style()
{
}

StylePtr Style::getDefaultStyle()
{
	return g_defaultStyle;
}

void Style::setDefaultStyle( StylePtr style )
{
	g_defaultStyle = style;
}

/*
const std::string &Style::stateAttribute()
{
	static std::string s = "user:GafferUI:state";
	return s;
}

IECore::ConstDataPtr Style::stateValueNormal()
{
	static IECore::DataPtr d = 0;
	if( !d )
	{
		d = new IECore::StringData( "normal" );
	}
	return d;
}

IECore::ConstDataPtr Style::stateValueInactive()
{
	static IECore::DataPtr d = 0;
	if( !d )
	{
		d = new IECore::StringData( "inactive" );
	}
	return d;
}

IECore::ConstDataPtr Style::stateValueSelected()
{
	static IECore::DataPtr d = 0;
	if( !d )
	{
		d = new IECore::StringData( "selected" );
	}
	return d;
}
*/
