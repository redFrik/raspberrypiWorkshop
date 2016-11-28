(
s.waitForBoot{
	var syn, ser, r;
	syn= {|freq= 0| SinOsc.ar([400, 404]+freq, 0, 0.2)}.play;
	ser= SerialPort("/dev/ttyUSB0", 57600);
	r= Routine.run({
		var val;
		inf.do{
			var data= [];
			var d= 0;
			while({d!=255 and:{d.size<100}}, {
				d= ser.read();
				data= data++d;
			});
			if(data[0]==253 and:{data[1]==254}, {
				val= (data[2]<<8)+data[3];
				syn.set(\freq, val);
				val.postln;
			});
		};
	});
	CmdPeriod.doOnce({ser.close});
};
)