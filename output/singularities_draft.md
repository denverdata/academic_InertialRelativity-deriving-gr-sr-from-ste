# Title: The Fallacy of the Arbitrary - Exploring the Mathematics and Interpretation of Infinities and Singularities

# Abstract

A common mathematical error is regularly invoked in the context of general Relativity, cosmic expansion, and other phenomena we observe. And this error relates to a declaration of division by 0 and, therefore, a blow-up of a particular formula or function. Specifically, this suggests that if something is very small from our perspective, we can neglect its contribution. And from this one small presumption, we impart a logical fallacy, a mathematical error, and also carry forward a physical misunderstanding. It is to contrive an artificial zero from a number that seems subjectively very small, such that one can declare division by zero or blow up. The explanation for the failure, whether a blow-up, division by zero, or any other number of creative descriptions, always roots in the same logical basis. That something is infinite and therefore something else is zero, and therefore a division by zero occurs, and therefore a system has blown up or gone out of its usable range or has transitioned to another model or any number of different wording that might be used. In each and every case, the formula presented is valid for every valid input. Meaning, if you want to know its value at 1 x 10^googol, you can do that and get a finite number back. In this paper, we provide a categorical decomposition of these arguments and explore their proper interpretation and calculation. From this, we demonstrate that there really is no physical interpretation of a point mass or mass singularity that has any factual basis. Mass must always accompany spatial distribution. While it may feel negligible from some perspectives, it truly is not.

# Introduction

There is a natural tendency for anyone observing the universe to see things only from their own perspective, which is entirely understandable, because that's the only perspective from which they can observe. But as we learn, we realize that anything can be observed by anyone, and those observations are dependent entirely upon the perspective from which it's observed. Describing the same system from two different observational perspectives. We have been guilty many times of extending ourselves a privileged position in the universe. Each time we cross a more nuanced bridge, we must again humbly accept our insignificance. There was a time when we thought the Earth was the center of the universe. Why? Because that's how it looks to us, and we've never looked at it from anyone else's perspective. Spatial scale and physical phenomena associated with such represent the next frontier in physics, from which vast knowledge, clarity, and opportunities will emerge. Not too long ago, we believed that atoms were the smallest unit of matter. We know now that that presumption was incorrect, and we have continued to reveal smaller constituent particles, each of which we, for some period of time, believe is the fundamental unit of matter. 

As is evidenced by the two examples above, humans commonly define anything beyond the periphery of what we can observe as non-existent. If I reach deep, it feels born of existential protectionism; kid gloves for our egos. Something analogous to hiding under a security blanket to protect yourself from the thunder. The unknown is unsettling, and our ego prefers the safety of complete knowledge. But again, the fundamental reason is that it's easy to presume that the only perspective we have is the only perspective there is. Self-deception would be very difficult to detect in such circumstances, especially with a significant payout in the form of psychological comfort. These are recurring themes for the pervasive mathematical challenges I describe herein.


## Looking to the stars

If we look up at the night sky, most stars don't stimulate more than one cone (the light detector) in our eyes, which means, from our perspective, a star could get no smaller; it's a point. We see their celestial behavior, so we know celestial objects have mass. Without more information, it would be easy to assume that these could be only point masses. Well, that's not true, but it's approximately true from our perspective. But if we were to look at how things behave leading up to that limit of detection, they're extremely consistent. If we presumed that the only change at the edge of our ability to observe was simply our ability to observe, we would have a much clearer understanding of the universe than we do under the weight of presumed boundaries. We must resist the tendency to think only in terms of our perspective, because that's where the fallacy lies. We should look at the trends and ask ourselves: why would the trends stop? Why would spatial extent cease to exist beyond some scale if it existed observably all the way to that scale? 

The simple answer is: It does not cease to exist. It just ceases to be visible to us from our scale of observation, for a variety of reasons. And thus one should never trust one's instinct to disregard something that feels insignificant. To presume negligibility, and then to extend that by rounding to zero, and therefore producing a division by zero error. It's a faulty multi-step logical construct. The commonly used terms "negligible," "arbitrarily large," "very small," and "singularity," are all red flags for potential misunderstanding. signifying that many people today are still at risk of accepting or even representing, God forbid, the "fallacy of the arbitrary" as factual interpretation.


# Review of Mathematical Concepts
Before we dig too deep into the various arguments represent imcorrect usage or conclusions, let's briefly review some relevant mathematical concepts. The following are more or less the "dictionary definitions" followed by an example that demonstrates the proper usage and interpretation.

## Asymptotic Limit

**Definition:**
In analytic geometry, an asymptote of a curve is a line such that the distance between the curve and the line approaches zero as one or both of the $x$ or $y$ coordinates tends to infinity. More generally, it describes the limiting behavior of a function as it approaches a value where it may be undefined. It is the mathematical formalization of a direction of travel rather than a destination; the curve and the asymptote approach each other "at infinity," meaning they get arbitrarily close but the gap never truly closes within any finite range.

The following excerpt describes the complexity of understanding asymptotic limits.

> "The idea that a curve may come arbitrarily close to a line without actually becoming the same may seem to counter everyday experience. The representations of a line and a curve as marks on a piece of paper or as pixels on a computer screen have a positive width. So if they were to be extended far enough they would seem to merge, at least as far as the eye could discern. But these are physical representations of the corresponding mathematical entities; the line and the curve are idealized concepts whose width is 0. Therefore, the understanding of the idea of an asymptote requires an effort of reason rather than experience."
>
> — *Asymptote*, Wikipedia Encyclopedia (https://en.wikipedia.org/wiki/Asymptote)



**Mathematical Representation:**
The behavior is defined using the limit notation:
$$\lim_{x \to c} f(x) = L \quad \text{or} \quad \lim_{x \to \infty} f(x) = L$$
Where:
- $c$ is the point of approach (vertical asymptote).
- $L$ is the value the system trends toward (horizontal asymptote).

This notation emphasizes the *process* of approaching. It explicitly avoids the error of stating $f(c) = L$, which is often where the "division by zero" or "singularity" fallacies are introduced.

**Behavioral Discussion:**
The asymptotic limit describes the behavior of a function as it nears a boundary without ever requiring the function to occupy that boundary. For every finite input $x$ leading up to $c$, the function $f(x)$ produces a finite, tangible output. The error in many interpretations lies in treating the limit $L$ as a value attained at a specific coordinate, effectively "rounding to zero" the remaining distance. This ignores the infinite progression of values that exist as $x$ approaches $c$. There is always a "universe of consideration" between the current state and the limit; to collapse this distance is to commit the fallacy of the arbitrary.

**Example: The Inverse Scale**
Consider the function $f(x) = \frac{1}{x}$. As $x$ approaches $0$ from the positive side, $f(x)$ increases toward infinity.
*Analysis:*
If we choose an $x = 10^{-100}$, $f(x)$ is $10^{100}$. Whether we label this value "massive" or "negligible" depends entirely on our chosen scale of reference; if our units are $10^{100}$ meters, this result is merely $1$. If we move to $x = 10^{-1,000,000}$, the output is $10^{1,000,000}$. This is $10^{999,900}$ times larger than the previous state, yet it remains finite. The "singularity" at $x=0$ is never reached because $x$ can always be halved, and halved again, forever. The trend toward infinity is the asymptote; the perceived "blow-up" is merely a failure of the observer to maintain a consistent relative perspective as the scale shifts.

## Negligibility

It is common for people to think of negligibility from their perspective, which is a typical human-centric way of looking at things. There's nothing wrong with that perspective. It's 100% correct, just like any other perspective. However, making a presumption of negligibility based on one's own scale invites mathematical problems. You might say that 1e-50 meters is extraordinarily small, but it's not compared to 1e-100 meters. For every number that you can cite, I can cite one that's bigger or smaller in every single circumstance forever.

Where could this become a problem? When you are dealing with numbers that are outside of the human scale, there is a tendency to discard those, and you can't do that. You need not ever assess whether something is negligible; the math will take care of that for you. If you use scientific notation and maintain full precision until the end, and then round to the appropriate number of significant figures. And you will never run into a problem of negligibility or infinity, because things are never negligible or infinite. One can always come up with something more negligible than that.

**Example:**

In classical mechanics, the Lorentz factor γ = 1/√(1 - v²/c²) differs from 1 by the amount v²/c². For everyday velocities (v = 100 m/s, c = 3×10⁸ m/s), this gives v²/c² ≈ 10⁻¹³. Physicists routinely drop this term entirely, declaring it "negligible," setting γ = 1 exactly. But 10⁻¹³ is not zero. At sufficiently precise measurements or over sufficient time/distance scales, this "negligible" term accumulates to measurable effects. The term was discarded based on human scale intuition, not mathematical necessity.

## Infinity

Infinity is a tough concept, but I think of it like this: it's not a number; it's the absence of a boundary. It's an absence of an upper boundary. In this context, to declare something that is arbitrarily large as infinity is a fallacy. There's no number that equals infinity because for every number you can give me, I can come up with one that's much larger or much smaller forever, infinitely. In this case, infinity is the thing you approach forever. And in fact, it often is the limit to an equation, to many equations. That is the limit. Something will go to infinity. That doesn't mean it ever attains infinity. That means there's no boundary to how big it can be at any given time. If you think of things contained within a box, the boundary is the box. Something that is contained within infinity doesn't have a box around it. So infinity isn't the number, it isn't the box, it's the absence of the box. You could fit an infinite number of boxes in infinity. You could fit an infinite number of infinities within infinity. Because infinity isn't a number. It's the absence of a boundary. In mathematics, infinities are not attainable because they're not a number.

**Example:**

The Schwarzschild metric for a black hole contains the term (1 - 2GM/rc²). As radius r approaches zero (r → 0), this term approaches negative infinity, and its reciprocal approaches positive infinity. Physicists claim this represents a "singularity" where the mathematics "breaks down." However, r never actually equals zero—it approaches zero as a limit. The metric remains mathematically valid at every finite r value, no matter how small. The claimed breakdown occurs only when they incorrectly treat the limit as an attained value.

## Division by zero

Division by zero is, in fact, a mathematical error. However, I would describe this as a mathematical error on the user's part. If there were instructions that came with division, they would surely say something like: “Warning, do not use this formula to calculate the fraction of a set of none, because you will get a meaningless answer.” As you can imagine, conceptually, to take the fraction of something that doesn't exist is nonsensical.

If you have used a calculator, dividing a number by zero simply requires you to enter the number, press the “÷” symbol, then the zero symbol, and hit Enter (presuming standard calculator notation). It will return a division-by-zero error. Before the advent of the calculator, you would have been using long division with a pen and paper. In those days, you wouldn't take the time to do a calculation on paper before you knew very clearly what it was you were trying to take a fraction of; it was just too much effort to make frivolous calculations. But there was also a world where calculating high-precision things was a lot of work. A lot of work. And it may have seemed attractive to accept certain mathematical inconsistencies. it is very possible that he will have gone into the problem knowing exactly how precise that zero is, If you're doing floating-point math on a computer, it's going to return infinity or give you an out-of-range error because the result is an arbitrarily large number—not arbitrary in the sense that it's meaningless, but arbitrary in the sense that it can't be represented. There are just too many digits to carry around for any regular system of precision. That said, to ever round a number to zero in order to arrive at such an error is a fallacy. I would advise people to let the mathematics do the work rather than trying to impose human judgment into the process. Stated simply, if no one were ever to make the mistake of rounding a very small number to zero in order to arrive at a division by zero error, we would have solved many of the misconceptions associated with the most fundamental principles of the physical universe. These misconceptions are far-reaching and pervasive.

To explain further, in computer science, there is the notion of floating-point arithmetic—that is, arithmetic that does not involve integers. In that world, which is every bit as accurate a way to describe our universe, everything is always some infinitely precise variant that could be very close or not to integer values. In integer operations, where one divides something by zero, that zero is interpreted to be a literal zero with infinite precision—an integer version of zero. It's a non-number; there's no number there. That's a world where division by zero may have meaning. But in the world of floating-point, there's no such thing as an integer zero, unless defined as such. Floating-point mathematics treats everything as scientific notation and presumes that even though you can't represent infinite precision, that infinite precision exists. As such, you would never see a zero on the denominator for any equation. You would see something that was perhaps a very, very, very small number. At some point, the number gets so small that the computer can no longer represent it. In computer science, for standard double-precision computing, a typical limit for numerical representation would be an exponent of ±308—that is, approximately 1e±308. That's an extraordinarily large or extraordinarily small number. 10^100 is a googol. A googolplex is probably the biggest number you would ever need to use in calculations involving human matters. That's not exactly true, but it is fairly accurate. You can use more than that, but you won’t go much higher. The ±308 range is a pretty safe bound. In this world, you will never get a division by zero error, because it doesn't exist. Properties in the natural world are always infinitely precise, limited only by our ability to observe. Thus, division by zero, as I stated, could never be reported—it could not be attained. The error would be one that refers to a number outside the representational bounds, meaning a number smaller than approximately 1e-308 or larger than approximately 1e308. That's a 1 followed by 308 zeros, or preceded by 308 zeros.

Comparison of floating-point “division by zero” responses by language:

*   **Python**: OverflowError: (34, 'Numerical result out of range')
    
*   **C/C++**: Returns ±HUGE\_VAL or ±INFINITY, sets errno to ERANGE
    

Modern computing and floating-point mathematics make clear that division by zero is an unacceptable natural circumstance. It's a false assertion of error when we're really just talking about something that's too big or too small to represent, and never so small that it becomes undefined. A division by zero error is a mathematical impossibility in nature.

**Example**:

The electric field at a distance r from a point charge is E = kQ/r². As r approaches zero, physicists might round small r values (say r = 10^-200 m) to exactly zero, claiming a "singularity." However, E = kQ/(10^-200)² = kQ × 10^400 exceeds representable bounds and produces an overflow error, not division by zero. The calculation remains mathematically valid—the computer simply can't represent the result. Only by artificially inserting r = 0 does the false "division by zero" appear. Please double-check responses. For every finite input, there will be a finite output. Infinity and zero should not be interpreted as actual numbers, but rather as the absence of boundaries. One approaching zero, and one approaching infinity.

## Divergence

Divergence reflects an actual mathematical phenomenon. For a function like y = 1/x, as x approaches zero, y approaches infinity. In both cases, these represent limits approached asymptotically—neither is ever attained. When you're looking at a standard x-y graph of y = 1/x (for positive x), it's easy to visualize infinity extending off to the right along the x-axis, but it's not so easy to visualize the corresponding infinity along the y-axis as x approaches zero from the right. The function never reaches x = 0. As it gets arbitrarily close, the y-values grow arbitrarily large. Far to the right, the graph appears nearly flat—very small increments in y for large changes in x. But near zero on the x-axis, very small increments in x produce enormous changes in y. This is divergence: unbounded growth as the function approaches a limit.

That said, to my knowledge, this divergence still returns a finite output for every finite input. There is no system, no matter how small or large, that cannot be modeled, with appropriate precision. It is not, under any circumstances, a tangible indication of transition to another model or a failure of the existing model.

**Example**:

I<Need an example GR, but plot arbitrary large values to plot the curve>

Conclusion: Summarize key insights.all systems must have both mass and extent.

Implications and Opportunities: Consider high level implications and next steps for this research. Wha new questions can now be asked or answered under this undersanding? Does it represent a significant shift in our understanding of physics? How will we need to revise our models or theories, and what are the implications of those revisions?


# Review of Physics Principles

## The Relativistic Regime

Classical physics is just relativistic physics without the added precision needed at extreme scales . so one need not delineate those two as separate regimes. We simply learned about one before we learned about the details we were missing at near-scale.

## Quantum Regime

Again, there is no actual transition to another regime. These are two equally accurate ways to look at things, one of which is very difficult to observe unless you get a huge difference in scale, and the other is very difficult to observe if you get too big a difference in scale. They are both correct. They describe the same universe. <only touch on this>

## Planck Scale

The Planck scale is often erroneously cited as a cutoff beyond which one cannot use classical relativistic formulas. I do understand that there is an observational perspective from which quantum is the only meaningful way to look at things, due to observational challenges. But that doesn't state, or even imply, that the Planck scale is that point. In fact, there's no indication of a point. I don't think the conclusion of the Planck scale was that it was the minot scale or the minot scale at which you could make relativistic measurements. And I don't think your statement would be true either. The Planck scale is considerably smaller than the scale at which we have to transition to indirect observation. So it probably means something slightly different from that. It may not mean much; it might just be the convergence point of three different formulas he cross-referenced. Not heard anybody explain to me what that number actually means other than they've implied that it's the minimum, and I know that's not the truth. Or, there is no reason to believe that that's the truth, despite the fact that we have not observed anything in that range. look this up.

# Subjective Declarations of Insignificance

One class of fallacy I describe as “Subjective Declarations of Insignificance”

Commonality: these all reflect a relativistic declaration, like "big" or "small," that is not necessarily relevant to the question at hand. Those kinds of terms have no meaning without a rational comparator, and the scale of the person making observations is not necessarily the best comparator. To presume negligibility or infinities without letting the math speak for itself is a perilous territory.

To mitigate this fallacy, use scientific notation. Never round something small to zero. Never honor an inadvertently contrived division by zero. Never make making a judgment call based on a perceived divisionn by zero, but rather to go back and rethink the mathematical nature of the decision you're trying to make. Or the experiment you are conducting. The correct treatment is to never make judgment calls about your inputs before you work the math. Let the math and the formulas do that out for you.

There are two commonly cited versions of this fallacy:

**"Arbitrarily large"** - Declaring something arbitrarily large without a comparator, or any quantification, is largely meaningless. the implication is that something is so large that any large value you pick would have the same result.

**Example**: In general relativity, we refer to the zero-time-dilation state as "an arbitrarily large radius." However, the “arbitrarily large number” you pick for that radius affects the time dilation figure in a way that would have significance on the types of calculations we'd need to do. Time dilation factor between the International Space Station and the surface of the Earth is extremely small yet, it has a very real meaning in terms of how many seconds per unit of time a clock would be off between the two systems .

**“Arbitrarily small“** A value so small that you consider it to be negligible is often rounded to zero, and this denominator creates a division by zero. You round it to zero, and you get a division by zero. This represents a mult-step error. To arbitrarily round to zero only to declare a mathematical error is not logically coherent.

## subjective declaration of a model becoming uncontrolled or unpredictable

This category encompasses all of the notions of something blowing up or going wildly out of control, or no longer matching the model because it's becoming random. Anything like that. Things that are just diverting too far really, what this describes is cases where the curve/plot diverges, meaning it goes up to extreme levels of x-values in order to get closer and closer to a 1 over x-value of zero. I've heard lots of terms for it, but in every case, it is a fully valid model all the way to it's limit. there is no case where the formula returns a random or inconsistent value from a regular finite input, however big or small. It is always a subjective interpretation that is used to pre-emptively disclaim a meaningful calculation.

The variants of thsi fallacy are:

"becomes unpredictable", " becomes chaotic.", “blows up” or “diverges”

Divergence never really results in chaotic or unpredictable behavior. It might appear unpredictable. It might be exceedingly complex. But I believe that, in every case where this is stated, you would still get a finite output for every finite input, and one that makes sense, not a random result.

## Subjective declaration that a system has transitioned to a different model, or that the model is no longer applicable

## Declaration that the model is no longer valid for this range of input

We've transitioned to a new scale regime the old formula is no longer valid

The Quantum Regime

This group of narratives represents the perspective that there is a threshold, after which you must honor a different set of formulas, and I believe this is erroneous logic. This is a preemptive disclaimer of a failing formula that doesn't really fail in favor of one that you think is more real. In actuality, they are both fully accurate and valid systems, but they measure things in completely different ways because they are observationally different. Represent two completely distinct models of observation:

One that has to do with discrete objects

One that does not have to do with discrete objects  
The second one has to do with random samplings of discrete objects that have discrete values, but they're not the same discrete object each time you sample.

So then they will disclaim that they don't really mean a literal singularity, only a sign that it moves to some different model, that the model is no longer explained mathematically by the former scale's model. And then they say that it was an ideal thing and that that's not really how the natural world works. most often, real to classical or quantum mechanics are cited in these circumstances however, there's no indication that quantum mechanics stops at a particular threshold, nor that relativistic physics starts at a stop at some threshold. they do accurately reflect the limits of our ability to observe directly.

"Transitions to a new model."

"Is no longer applicable."

## Declaration that there is no interpretation of singularity

This group of arguments for the logic we're discussing herein pertains to parties who choose to misrepresent their own position on the topic and really doesn't apply to anyone else. These are not actual arguments for or about mathematics; they're semantic arguments about whether somebody really said they believe something or whether they just use it as an analogy or as a vehicle to understand something. And so I would say that if we're talking about something like the center of mass, where you're describing a location and not a real system, that absolutely applies. But if you're describing something where something is at some point in its existence, either in the future, in the past, or currently, under certain circumstances, it obtains a singular or infinite state. I cite the mathematical fallacies described herein.

“It's an idealization”  
Only narrowly distinct from being an analogy. There are cases where a concept is used for an idealization of another concept. So in this case, an idealized system goes to infinity or goes to zero. But that's just not true. That's not true in this case. Nor does it serve as a utility from an ideal perspective. Nor is it really done. Not correct anyway.

This is useful and with the abstraction of the "center of mass" as a relative location, but not in any other regard is that literally the case. For, to invoke it necessarily implies that one believes it to be attainable and meaningful.  
It transitions to a different model

It's an analogy  
To claim mere analogical use, while simultaneously trying to demonstrate the age of the universe or some degree of persistent cosmic expansion, that's not an analogy; that is a literal interpretation of that trajectory.  
Not literally saying a singularity.

## Asserting that the mathematics and physics aren't necessarily aligned

I consider this category to be another disclaimer from doing the math in the first place. Or from being able to draw conclusions from the math. This is a wild claim that I think is completely baseless.

“Physics doesn't necessarily match mathematics.”  
Nature is the thing that we model mathematically, and while we may not understand how to use all of the math, it all can be represented mathematically. That said, the universe is infinitely precise with every property a system could possess. Our ability to observe and measure these properties is vastly more limited in precision and accuracy.

* * *

## Appendix A

## A Note on the Author's Qualifications and Methodological thinking

Tom DeGerlia has spent his entire lifetime thinking about time and space at all scales. He pursued chemistry, physics, biology, and mathematics, eventually earning a Bachelor of Science in Chemistry and Mathematics. While never a valedictorian, Tom took time to learn from every experience, whether academic, professional, or personal. He learned early on that to solve a problem, one must clearly understand it. And to understand a problem in detail, one must ask many dumb questions. This led to the inception of a strategy for objectivity that he leverages every day. This is based on the following principle:

> "Every time I ask a dumb question, as long as the answer is available, I learn something. But if I pretend to have no questions because I do not want to look dumb, I have declined that opportunity. Which does not serve the goal of intelligence."

As Tom's career path led him through analytical chemistry (mass spectrometry), through software engineering, and to AI research, and AI-augmented physical research, he continued to assemble key principles for his objectivity toolkit:

#   Observations are vastly more reliable than conclusions. Conclusions are really just a "hypothesis of explanation" that, much of the time, has little or no bearing on that which it seeks to describe. They are conjecture. Observations are generally not.
    
#   The person seeking the solution will have a bruised ego if someone is able to solve the problem they could not. That draws their observations into question. For example, someone might say, "Oh, I already tried that," apparently to deter me from having to repeat any of their highly reliable work. Most of the time, the solution lies plainly behind that sleight of hand or, at best, could not be diagnosed without a clear and honest picture.
    
#   Others involved in a solution are of questionable reliability and will often use social techniques to obscure a solution. People see other capable people as a competitive threat to their self-perception or for making it more difficult for them to achieve success. They will utilize every logical fallacy, refuse to review, refuse to respond, refuse to acknowledge, refuse to concur, explain principles incorrectly, or otherwise obstruct or leave toothless any perceived threat, to the extent that the social risks do not exceed the benefit of the competitive effort. Meaning any obstruction will be covert.
    
#   Take nothing for granted. Often, the extremely accepted or well-defended things in science amount to misconceptions, false conclusions, or misunderstood boundaries. For example, the speed of light has been measured many times to reasonably high precision, but it does not therefore follow from this information alone that light is a massless particle that travels from source to destination.
    
#   As you illuminate a problem, collect facts. (Newton would have had difficulty making the discoveries he did if he had accepted the prevailing science in full at the time.)
    
#   Hypothesize and evaluate using analogies. Many patterns in nature repeat in ways that allow one to predict an object's expected behavior.
    
#   If an explanation feels sketchy, it is generally because we do not fully understand it. Or at least the person explaining does not understand it. Things in the actual world have consistent explanations, consistently. Usually, they are simple because, again, something overly confusing to understand often represents a confused perspective, not a truly confusing principle.
    
#   Accept no logical fallacies, which is why observations are so valuable; they tend to contain fewer of these.
    
#   Remember, just as Relativity allows for multiple correct perspectives on the same thing, it is okay to open one's mind to new perspectives logically. You can trust that your logic machine will not let you get tricked simply by pondering a new concept.
    
#   Above all, do not trust yourself. Your ego will deceive you at every turn, for countless reasons that are distant from your conscious objective. If there is anything in your interest that would be better served if you believed some small mistruth, you will do that. _I use the exercise of taking the counterpoint and testing whether I can defend it with the same vigor; if I can, my conclusion is suspect._ Be conscious of your feelings; if I get offended, angry, or defensive, it touches on some insecurity of mine, and my opinions are suspect.  

So, as you read this exploratory paper, I want you to logically scrutinize every fact or conclusion, but try to resist arbitrarily dismissing them. Give yourself the opportunity to explore where discoveries are made: beyond the current understanding. I will defend every assertion conversationally and can and do regularly revise my position in response to arguments, analogies, or experiences.

remove this when done



 

Zero, Infinity, and Asymptotic Limits

$$\text{As } x \to \infty, \; \frac{1}{x} \to 0$$

If somebody says, "as x goes to infinity, 1 over x goes to zero", they're making a statement about an asymptotic limit. I.e., means that a function approaches some limit as the input approaches zero or infinity. That's not to imply that infinity is a number; on the contrary, infinity describes the absence of a finite boundary. For every arbitrarily large number you could suggest, I could come up with a number one order of magnitude larger forever. 1/infinity works the same; infinity is still unbounded, it's the same infinity; it's 1 over the same number. But again, it's never infinity, it's never 0. Visually, 1/x plots on a x/y graph as a line that turns upward sharply at 1 and gets almost completely vertical as it gets ever closer to zero. It looks like a wall, but it is not. It's just the same as the infinity on the other side, just represented differently. There is no valid finite input that you can inject into that equation that does not return a finite output. 

<show a graph of x vs 1/x>

In this context, both 0 and ∞ are not numbers but rather are the absence of a boundary.

The absence of a boundary for how small the number can get fractionally, which is unlimited.

A limit to how far it can go, its extent, and that is unlimited. 

It does not, in any way, suggest that these values ever reach zero or infinity, because zero and infinity are not numbers in this context. They are simply the absence of a boundary. An asymptotic limit is the thing you approach infinitely, but can never reach or go beyond. By definition.

What is a divergence

  **

Math associuated with singularities and limmits

What is a asymototic limit? As x->infinity, 1/x->0

Floatin poin math does not allow the value 0 literally. It is not a valid value.

Rounding to very small values to zero

Division by zero errors

Planck Scale

For everty finite input, there is a finite output. 

Infinity is not a valid input or output. It is not a number. Nor is it a true zero in this context. Both represent the absence of a finite limit.

Types of "singularity" erroneous arguments

Asymptotic limit interpreted as attainable - division by zero

Infinity limit interpreted as a number - diverges or rapidly becomes unpredictable, chaotic, unstable, or infinity

Arbitrarily large/small - logical misconceptin about the nature of Relativity

Quantum/Planck scale neither says relativistic no longer applies.

Coordinate singularities - not a singularity, and further, the event horizon does nto represeent zero time, it;s just where visible light cannot excape.

Normalization of time dilation under gtd.

Electric current calculations

Specific Examples with valid Interpretation

Black hole singularity  - asymptotic limit, coordinate singularity

Cosmic expansion singularity - can not exist, or is an asymptotic limit at best.

It diverges - For every finite input, there is a finite output. 

A different model applies - quantum vs. relativistic - both models coexist, it is an observatonal phenomenon. - leave quantum out of it.

Turbulent vortices - Navier-Stokes Conjecture

UV catastrophe - It did not exist. Reinterpret using the classical formula.

Arbitrarily large or small is not a real thing. Something can be negligible relative to something. 

GTD Normalization of time dilation??? (no now )

The model fails at some scale - incorrect math

Electric current calculations

Carnot principle
