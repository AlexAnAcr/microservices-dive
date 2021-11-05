using System;
using AudioSwitcher.AudioApi.CoreAudio;

namespace ExpressionLineProcessor {
    class Program {
        static void Main(string[] args) {
            {
                CoreAudioDevice defaultPlaybackDevice = new CoreAudioController().DefaultPlaybackDevice;
                defaultPlaybackDevice.Volume = 0;
            }

            ServerAPI.MicroService serv = new("http://localhost:8080/got", "http://localhost:8080/gave", true);
            NetCoreAudio.Player player = new NetCoreAudio.Player();

            while (true) {
                string input = serv.GetJob<string>("Demo.Backend.ExpressionLineProcessjor.Handle", out ServerAPI.ResponseAddress addr);

                Console.WriteLine("MutliExpressionCalculator input: " + input);
				
				//V2lWZSwgV2luVmVyOiBXaW5kb3dzIFVua25vd24gVmVyc2lvbnM7

                if (!player.Playing) {
                    if ((DateTime.Now.Ticks & 1) == 1) {
                        player.Play("Secret Song 1.mp3");
                        Console.WriteLine("Челлендж: попробуйте определить, о чём эта песня, на слух.");
                    } else {
                        player.Play("Secret Song 2.mp3");
                        Console.WriteLine("Челлендж: попробуйте определить, о чём эта песня, на слух.\nИсполнители этой песни всемирно известны, вы должны были как минимум, слышать о них.");
                    }
                }

                Console.WriteLine("MutliExpressionCalculator output is same. LUL, I just playing music =)");

                serv.PostIntermediateResult("Demo.Backend.ExpressionLineProcessor.Handle", addr, input);
            }
        }
    }
}
