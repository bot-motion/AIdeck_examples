# Docker images to work with AI Deck by bitcraze

Check out the [documentation](https://www.bitcraze.io/documentation/repository/AIdeck_examples/master/)
for starting guides. 

The AI deck for the quadcopter crazyflie by bitcraze.io requires the setup of dev toolchains for its GAP8 chip and its wifi chip ESP NINA.

To automate building projects with the AI deck using Github actions, we need docker images for the [GAP SDK](https://github.com/GreenWaves-Technologies/gap_sdk/), [ESP NINA](https://github.com/bot-motion/AIdeck_examples/blob/master/docs/nina-instructions/docker-nina.md)  and [bitcraze's builder](https://hub.docker.com/r/bitcraze/builder).

The resulting docker images are

[GAP SDK](https://hub.docker.com/r/simatai/gapsdk)
[ESP IDF NINA](https://hub.docker.com/r/simatai/espidf)
[STM bitcraze builder](https://hub.docker.com/r/bitcraze/builder)

Note that the GAP8 SDK's autotiler has a user-bound license that's not activated inside the docker image. Follow the [steps outlined by bitcraze](https://github.com/bot-motion/AIdeck_examples/blob/master/docs/getting-started/docker-gap8.md)

## More information

Check out the [documentation](https://github.com/bitcraze/AIdeck_examples/tree/master/docs) folder for starting guides. Also consult the github presence of [Greenwave Technologies](https://github.com/GreenWaves-Technologies/gap_sdk/) 
