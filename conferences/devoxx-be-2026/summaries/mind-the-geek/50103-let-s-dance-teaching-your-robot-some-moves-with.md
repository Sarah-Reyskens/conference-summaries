---
title: "Let's dance! – Teaching your robot some moves with reinforcement learning"
talkId: "50103"
conference: devoxx-be-2026
speakers: [Thomas Endres, Martin F., Tobias Lübbe]
track: Mind the Geek
sessionType: Lunch Talk
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=gPtWq_LHL8o
durationMin: 41
slides: null
verdict: 7
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Let's dance! – Teaching your robot some moves with reinforcement learning

Thomas Endres, Martin F., Tobias Lübbe · Lunch Talk · Mind the Geek

## TL;DR

Three engineers from TNG's innovation hacking team describe how they taught a Unitree G1 humanoid to walk and dance with reinforcement learning: RL basics, standing and walking policies in NVIDIA Isaac Sim, motion retargeting from human video, and the sim-to-real gap. The talk ends with generalist motion-tracking models (NVIDIA SONIC) that imitate dances without per-dance training.

## Key takeaways

- Train humanoid policies against a digital twin in simulation (Isaac Sim); training on the physical robot breaks hardware.
- Reward shaping is the actual engineering: a pelvis-height reward produced an upward-dog yoga pose, and a velocity reward produced sack-race jumping.
- Human dance video cannot drive the robot directly because body proportions differ; the pipeline runs MediaPipe keypoints through SMPL into GMR retargeting (inverse kinematics onto the G1 skeleton).
- Test sim-to-real transfer with the robot hanging from a support rig, and expect the gap to widen as joints wear; randomizing actuator gains in simulation covers some of the drift.
- One imitation policy dances exactly one dance; generalist policies such as SONIC trade per-dance training for scaled-up networks, datasets, and compute.
- For 29 continuous degrees of freedom, tabular Q-learning is hopeless and actor-critic methods carry the load: the critic turns sparse rewards into a dense training signal for the actor.

## Notes

### [00:34](https://youtu.be/gPtWq_LHL8o?t=34) A EUR 50,000 party crasher

The speakers introduce TNG Technology Consulting's innovation hacking team, then the Unitree G1 humanoid Thomas Endres ordered from China for EUR 50,000 after a three-month silent wait. Out of the box it just stood there waving, while YouTube showed G1s dancing fluently. Those videos are cherry-picked, and the failure compilations show robots knocking people over, so the team wanted to understand the training before attempting anything.

### [04:09](https://youtu.be/gPtWq_LHL8o?t=249) Classical control is not the answer

Earlier NAO-robot work only mirrored a human lying on the floor. Zero-moment-point walking (keeping the center of mass between the feet) works but looks like decades-old Honda ASIMO footage. Caltech's model-based Cassie controller walks stably on small feet, yet it needs reduced-order models plus nonlinear optimization and only holds under lab conditions. The team chose reinforcement learning instead.

### [07:15](https://youtu.be/gPtWq_LHL8o?t=435) RL basics: Q-learning on the frozen lake

An actor in an environment takes actions, an observer scores them, and rewards or punishments shape behavior, illustrated with an IKEA table of intact versus broken boards. The frozen lake grid shows Q-learning live: random wandering until the first reward, propagation of Q values through state space, then a greedy policy that always takes the highest-Q action. Atari Breakout extends the same idea until the agent learns the tunnel-through-the-side pro trick.

### [14:05](https://youtu.be/gPtWq_LHL8o?t=845) Actor-critic for 29 degrees of freedom

Breakout has two actions; the G1 has 29 continuous joints. Actor-critic methods split learning into an actor mapping states to actions and a critic estimating long-term quality of state-action pairs, converting sparse rewards into a dense signal. OpenAI's 2019 Dota result sets the scale: five agents, 45,000 years of gameplay, 128,000 CPUs and 256 GPUs, enough to beat the world champions.

### [17:43](https://youtu.be/gPtWq_LHL8o?t=1063) Standing and walking in Isaac Sim

Unitree supplied a digital twin that runs in NVIDIA Isaac Sim. Standing rewards keep the pelvis at a set height with both feet down; after 6,000 steps the robot stands leaning, arms forward, because that pose balances easily. Walking adds a control signal (forward, back, left, right) with rewards for matching velocity and penalties for stumbling or jumping; on-screen arrows show measured velocity converging on the command. The walking policy then runs live on stage, the G1 striding while the speaker injects velocity commands. Bad rewards get exploited, as the yoga-pose and sack-race clips prove, so the final walking configuration is a long list of reward and penalty terms.

### [26:05](https://youtu.be/gPtWq_LHL8o?t=1565) From human video to robot dance

Two speakers demonstrate live that a dance cannot be described in words, which motivates motion capture. The pipeline extracts skeleton keypoints with a neural net (MediaPipe does this for video streams), converts them to SMPL format, then retargets onto the G1 skeleton with the open-source GMR kinematic solver. The team recorded their best in-house dancer ("the Benno") and trained an imitation policy with per-joint position targets per timestep; at iteration 10,500 the robot still looks drunk, then the motion converges.

### [31:21](https://youtu.be/gPtWq_LHL8o?t=1881) Sim-to-real: the hanging device and worn joints

Carpet, friction, and external forces differ from simulation, and one sim-trained policy failed on the real robot. Professional safety (a stopping harness, vision monitoring) looked expensive, so Martin built a wooden gallows rebranded as a "sophisticated robot hanging device". Suspended, the robot dances and recovers from hard shoves, though it stomps the operator's foot. A dynamic Fortnite dance exposes the widening gap, worsened by wear: the robot once drove a go-kart, and an opened joint showed ground-down gears and a burned-through cable. Fixes go both directions: randomize actuator gains in simulation, and repair the robot with epoxy and replacement joints. A Bavarian Schuhplattler dance then works on the hardware.

### [38:49](https://youtu.be/gPtWq_LHL8o?t=2329) Generalist policies: SONIC and outlook

Each imitation policy dances one dance, so the team tested NVIDIA's generalist SONIC model, which scales motion tracking on three axes: 300k to 42M parameters (140x), 30 seconds to 700 hours of motion capture (84,000x), and 4 to 21,000 GPU hours (5,250x), sourced to nvlabs.github.io/GEAR-SONIC. Fed a Hamilton dance video with no further training, the G1 performs it, and the team built a showcase that plays back dances on the robot now running SONIC. Future work targets useful tasks: carrying crates and playing soccer.

## Tools, libraries and specs

- Unitree G1 humanoid robot (29 degrees of freedom)
- NVIDIA Isaac Sim (simulation environment)
- MediaPipe (human pose keypoints from video)
- SMPL (human motion format)
- GMR, General Motion Retargeting (open-source kinematic retargeting solver)
- NVIDIA SONIC (generalist motion-tracking policy, nvlabs.github.io/GEAR-SONIC)

## Who should watch

Beginners curious how reinforcement learning meets real humanoids gain a full pipeline mental model plus concrete failure modes. Skip it for RL theory beyond actor-critic intuition, or for a code-level tutorial: reward terms appear on slides only as config fragments.

## Verdict

**7/10**: First-hand failure stories and a rig-tested real-robot dance walk a beginner through the whole RL-to-hardware pipeline, but the training setup is the vendor's repo and the team's own results carry no measurements or published artifact.

**Novelty 1/2**

- **+** [23:30](https://youtu.be/gPtWq_LHL8o?t=1410) The yoga-pose and sack-race reward exploits are the team's own failures, each with the reward change that fixed it.
- **+** [35:29](https://youtu.be/gPtWq_LHL8o?t=2129) The worn-gears autopsy and the two-directional sim/real realignment (randomized actuator gains, repaired hardware) come from the team's own robot.
- **−** The walking reward list at [25:03](https://youtu.be/gPtWq_LHL8o?t=1503) shares its terms and weights with unitreerobotics/unitree_rl_lab's g1/29dof velocity_env_cfg.py, which also ships G1 velocity and dance policies; a search for the subject reaches it, and the talk never names it.

**Demonstrated 2/2**

- **+** [33:25](https://youtu.be/gPtWq_LHL8o?t=2005) Real-robot video on the hanging rig shows the dance policy performing and recovering from hard external forces.
- **+** [39:52](https://youtu.be/gPtWq_LHL8o?t=2392) The Hamilton video runs through the SONIC policy with no further training and the actual robot performs it.
- **−** [34:27](https://youtu.be/gPtWq_LHL8o?t=2067) The dynamic Fortnite dance degrades on the real robot ("Feels a bit like the dance until it doesn't").

**Measured 1/2**

- **+** [39:20](https://youtu.be/gPtWq_LHL8o?t=2360) The SONIC slide quantifies the scale-up (140x parameters, 84,000x data, 5,250x GPU hours) with a source line, though these are NVIDIA's training inputs, not performance results.
- **−** [22:57](https://youtu.be/gPtWq_LHL8o?t=1377) The team's own walking and dancing results get no success rate or reward curve; training progress appears only as step counts (6,000 for standing, 10,500 for the dance).

**Depth 2/2**

- **+** [07:15](https://youtu.be/gPtWq_LHL8o?t=435) The actor/environment/observer model plus the IKEA reward table gives beginners a working mental model of RL.
- **+** [14:37](https://youtu.be/gPtWq_LHL8o?t=877) The actor-critic split is explained functionally: the critic turns sparse rewards into a dense signal so the actor can train.
- **+** [28:13](https://youtu.be/gPtWq_LHL8o?t=1693) The retargeting step says why direct transfer fails (human and robot proportions differ, the puppeteer's doll) and how GMR resolves it (inverse kinematics onto the robot skeleton).

**Reusable 1/2**

- **+** [28:45](https://youtu.be/gPtWq_LHL8o?t=1725) The pipeline names open-source pieces (MediaPipe, GMR, NVIDIA SONIC) a viewer can look up.
- **−** [25:03](https://youtu.be/gPtWq_LHL8o?t=1503) The team's own training setup appears only as a reward-term list on a slide; no repository or complete configuration is published.
