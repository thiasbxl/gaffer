##########################################################################
#  
#  Copyright (c) 2012, John Haddon. All rights reserved.
#  
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#  
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#  
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  
##########################################################################

import unittest
import threading
import weakref

import IECore

import Gaffer

class ContextTest( unittest.TestCase ) :

	def testFrameAccess( self ) :
	
		c = Gaffer.Context()
		
		self.assertEqual( c.getFrame(), 1.0 )
		self.assertEqual( c["frame"], 1.0 )
		
		c.setFrame( 10.5 )
		self.assertEqual( c.getFrame(), 10.5 )
		self.assertEqual( c["frame"], 10.5 )
		
	def testChangedSignal( self ) :
	
		c = Gaffer.Context()
		
		changes = []
		def f( context, name ) :
		
			self.failUnless( context.isSame( c ) )
			changes.append( ( name, context[name] ) )
		
		cn = c.changedSignal().connect( f )
		
		c["a"] = 2
		self.assertEqual( changes, [ ( "a", 2 ) ] )
		
		c["a"] = 3
		self.assertEqual( changes, [ ( "a", 2 ), ( "a", 3 ) ] )
		
		c["b"] = 1
		self.assertEqual( changes, [ ( "a", 2 ), ( "a", 3 ), ( "b", 1 ) ] )

		# when an assignment makes no actual change, the signal should not
		# be triggered again.
		c["b"] = 1
		self.assertEqual( changes, [ ( "a", 2 ), ( "a", 3 ), ( "b", 1 ) ] )

	def testTypes( self ) :
	
		c = Gaffer.Context()
		
		c["int"] = 1
		self.assertEqual( c["int"], 1 )
		self.assertEqual( c.get( "int" ), 1 )
		c.set( "int", 2 )
		self.assertEqual( c["int"], 2 )
		self.failUnless( isinstance( c["int"], int ) )

		c["float"] = 1.0
		self.assertEqual( c["float"], 1.0 )
		self.assertEqual( c.get( "float" ), 1.0 )
		c.set( "float", 2.0 )
		self.assertEqual( c["float"], 2.0 )
		self.failUnless( isinstance( c["float"], float ) )

		c["string"] = "hi"
		self.assertEqual( c["string"], "hi" )
		self.assertEqual( c.get( "string" ), "hi" )
		c.set( "string", "bye" )
		self.assertEqual( c["string"], "bye" )
		self.failUnless( isinstance( c["string"], basestring ) )

	def testCopying( self ) :
	
		c = Gaffer.Context()
		c["i"] = 10
		
		c2 = Gaffer.Context( c )
		self.assertEqual( c2["i"], 10 )
		
		c["i"] = 1
		self.assertEqual( c["i"], 1 )
		self.assertEqual( c2["i"], 10 )
	
	def testEquality( self ) :
		
		c = Gaffer.Context()
		c2 = Gaffer.Context()
		
		self.assertEqual( c, c2 )
		self.failIf( c != c2 )
		
		c["somethingElse"] = 1
		
		self.assertNotEqual( c, c2 )
		self.failIf( c == c2 )
		
	def testCurrent( self ) :
	
		# if nothing has been made current then there should be a default
		# constructed context in place.
		c = Gaffer.Context.current()
		c2 = Gaffer.Context()		
		self.assertEqual( c, c2 )
		
		# and we should be able to change that using the with statement
		c2["something"] = 1
		with c2 :
		
			self.failUnless( Gaffer.Context.current().isSame( c2 ) )
			self.assertEqual( Gaffer.Context.current()["something"], 1 )
		
		# and bounce back to the original
		self.failUnless( Gaffer.Context.current().isSame( c ) )
	
	def testCurrentIsThreadSpecific( self ) :
	
		c = Gaffer.Context()
		self.failIf( c.isSame( Gaffer.Context.current() ) )
		
		def f() :
		
			self.failIf( c.isSame( Gaffer.Context.current() ) )
			with Gaffer.Context() :
				pass
				
		with c :
		
			self.failUnless( c.isSame( Gaffer.Context.current() ) )
			t = threading.Thread( target = f )
			t.start()
			t.join()
			self.failUnless( c.isSame( Gaffer.Context.current() ) )
				
		self.failIf( c.isSame( Gaffer.Context.current() ) )
	
	def testThreading( self ) :
	
		# for good measure, run testCurrent() in a load of threads at
		# the same time.
		
		threads = []
		for i in range( 0, 1000 ) :
			t = threading.Thread( target = self.testCurrent )
			t.start()
			threads.append( t )
			
		for t in threads :
			t.join()
			
	def testSetWithObject( self ) :
	
		c = Gaffer.Context()
	
		v = IECore.StringVectorData( [ "a", "b", "c" ] )
		c.set( "v", v )
		
		self.assertEqual( c.get( "v" ), v )
		self.failIf( c.get( "v" ).isSame( v ) )

		self.assertEqual( c["v"], v )
		self.failIf( c["v"].isSame( v ) )
		
	def testGetWithDefault( self ) :
	
		c = Gaffer.Context()
		self.assertRaises( RuntimeError, c.get, "f" ) 
		self.assertEqual( c.get( "f", 10 ), 10 )
		c["f"] = 1.0
		self.assertEqual( c.get( "f" ), 1.0 )
	
	def testReentrancy( self ) :
	
		c = Gaffer.Context()
		with c :
			self.failUnless( c.isSame( Gaffer.Context.current() ) )
			with c :
				self.failUnless( c.isSame( Gaffer.Context.current() ) )
				
	def testLifeTime( self ) :
	
		c = Gaffer.Context()
		w = weakref.ref( c )
		
		self.failUnless( w() is c )

		with c :
			pass

		del c
		
		self.failUnless( w() is None )
		
	def testWithBlockReturnValue( self ) :
	
		with Gaffer.Context() as c :
			self.failUnless( isinstance( c, Gaffer.Context ) )
			self.failUnless( c.isSame( Gaffer.Context.current() ) ) 
	
	def testSubstitute( self ) :
	
		c = Gaffer.Context()
		c.setFrame( 20 )
		c["a"] = "apple"
		c["b"] = "bear"
		
		self.assertEqual( c.substitute( "$a/$b/something.###.tif" ), "apple/bear/something.020.tif" )
		self.assertEqual( c.substitute( "$a/$dontExist/something.###.tif" ), "apple//something.020.tif" )
		self.assertEqual( c.substitute( "${badlyFormed" ), "" )
	
	def testNames( self ) :
	
		c = Gaffer.Context()
		self.assertEqual( set( c.names() ), set( [ "frame" ] ) )
		
		c["a"] = 10
		self.assertEqual( set( c.names() ), set( [ "frame", "a" ] ) )
		
		cc = Gaffer.Context( c )
		self.assertEqual( set( cc.names() ), set( [ "frame", "a" ] ) )
		
		cc["b"] = 20
		self.assertEqual( set( cc.names() ), set( [ "frame", "a", "b" ] ) )
		self.assertEqual( set( c.names() ), set( [ "frame", "a" ] ) )
		
		self.assertEqual( cc.names(), cc.keys() )
		
if __name__ == "__main__":
	unittest.main()
	
