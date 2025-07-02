

import random
import streamlit as st
import functions
import math
import plotly.express as px
from collections import Counter
import plotly.graph_objects as go
from plotly.colors import n_colors
from scipy.stats import gaussian_kde
import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt

st.markdown('## *Shuffling cards:*')
st.title(" *A data-driven guide to improve your shuffling strategy*")
st.text("")
st.image('https://danq.me/wp-content/uploads/2014/10/poker-686981.jpg', width=800)
st.text("")
st.markdown("***There are many bugs and mathmatical errors still not fixed in this demo!!!***")
st.markdown("***It is also very slow bc no data were saved. Simulations are run every time one visit the site.***")
st.text("")

st.markdown(
    """ 
    I've always found shuffling cards to be a surprisingly stressful 
    task. How many times should I shuffle? Which technique is best? 
    How should I deal the cards afterward? And how can you tell if 
    the deck is truly well-shuffled? Everyone seems to have a 
    different answer. And if your poker buddies think you're not 
    doing a proper job by their standards, they might call you 
    out on it.

    So, what's a shuffling strategy robust enough to survive 
    peer review at the poker table?
    In this post, I’ll try to approach the question using 
    simulations. After all, math can get a bit intense 
    sometimes—and that’s where data can help make things more 
    intuitive.
    """
)


st.subheader("First, let's see a simple example", divider=True)


col1, col2 = st.columns(2)

with col1:
    deck = st.radio(
        "What kind of deck does your favorite poker game use",
        [ "**Complete Deck** 🂡🂱", 
         '**Standard Deck** 🃁 ',
         # ':rainbow[**UNO** ]'
        ],
        captions=[
            "54 cards",
            "52 cards without the jokers",
            # "108 cards",
        ])

    if deck == "**Complete Deck** 🂡🂱":
        n = 54
    else:
        n = 52

with col2:
    players = st.slider("How many players are there?", 2, 10, 5)
    chunk_size = st.slider("How many cards does each player get per deal?", 1, n//players, 3)


col1, col2, col3 = st.columns([5, 3, 1])

with col1:
    st.write(f'We have a {deck[:-3]} of unshuffled cards. If you wish to shuffle it completely, feel free to press the button on the right.')
    st.write(f'The {deck[:-3]} have **{n}** cards. With **{players}** players, you will be delt with **{math.ceil(n/players)}** cards.')

cards = list(range(n))

with col2:
    col21, col22 = st.columns(2)

    with col21:
        if "run_count" not in st.session_state:
            st.session_state.run_count = 0

        if "cards" not in st.session_state:
            st.session_state.cards = cards

        if st.button("Shuffle", type="primary"):
            st.session_state.run_count += 1
            # random.shuffle(st.session_state.cards)
            st.session_state.cards = functions.shuffling(st.session_state.cards, 
                                shuffle_proc=['gsr','hindu_shuffle','hindu_shuffle']*2, 
                                par_dict={'gsr': {'time': 1},
                                        'hindu_shuffle': {'location': 0.5, 'prop': 0.5, 'var': 2, 'time': 5},
                                        })

        if st.session_state.run_count ==0:
            words = f'**The card is unshuffled**'

        elif st.session_state.run_count==1:
            words = f'*The cards are shuffled 1 time.*'
        else:
            words = f'*The cards are shuffled {st.session_state.run_count} times.*'
        

    with col22:
        if st.button("Reset", type = 'tertiary'):
            st.session_state.run_count = 0
            st.session_state.cards = list(range(n))
            words = f'**The card is unshuffled**'
    st.write(words)
    
    dealing_bt = st.button('Dealing cards')






myhand = functions.dealing(st.session_state.cards, players = players, chunk_size=chunk_size)[0]
myhand = functions.show_cards(myhand)



if "myhand" not in st.session_state:
    st.session_state.myhand = myhand
if "run_count2" not in st.session_state:
    st.session_state.run_count2 = 0


container = st.container(border=True)
container.write('**Player 1\'s Hand**')


if st.session_state.run_count2==0 and not dealing_bt:
    container.markdown("""
                       <div align="center">
                       no cards being dealt ☹
                       </div>
                       """, unsafe_allow_html=True)
    container.write('')
elif dealing_bt:
    st.session_state.myhand = myhand
    st.session_state.run_count2 +=1

    row = container.columns(len(st.session_state.myhand), gap=None)
    i = 0

    for i, col in enumerate(row):
        card = st.session_state.myhand[i]
        if '♥' in card or '♦' in card:
            border_color = "#FF0000"  # red
        elif '♠' in card or '♣' in card:
            border_color = "#000000"  # black
        elif '🂿' in card:
            border_color = "#000000"
            card = '&#8202;'+card+'&#8202;'
        elif '🃟' in card:
            card = '&#8202;'+card+'&#8202;'
        with col.expander(card, expanded=True):
            col.markdown(
                f'<span style="font-size: {6+3*players}px; text-align: left; color: {border_color};background-color: #D3D3D3;">{card}</span>',
                unsafe_allow_html=True
            )

else:
    row = container.columns(len(st.session_state.myhand), gap=None)
    i = 0

    for i, col in enumerate(row):
        card = st.session_state.myhand[i]
        if '♥' in card or '♦' in card:
            border_color = "#FF0000"  
        elif '♠' in card or '♣' in card:
            border_color = "#000000"  
        elif '🂿' in card:
            border_color = "#000000"
            card = '&#8202;'+card+'&#8202;'
        elif '🃟' in card:
            border_color = "#FF0000"
            card = '&#8202;'+card+'&#8202;'
        with col.expander(card, expanded=True):
            col.markdown(
                f'<span style="font-size: {6+3*players}px; text-align: left; color: {border_color};background-color: #D3D3D3;">{card}</span>',
                unsafe_allow_html=True
            )

st.write('')

# st.write('The goal of shuffling as far as I can see is to randomize the card order for two main reasons)
st.write('''
         The shuffle I use here is based on a personal routine I’ve developed over time. 
         I start with one riffle shuffle, followed by two rounds of Hindu shuffling, 
         then repeat the entire sequence once more. From the demo above and my own experience,
         this approach seems to produce reasonably good results. But does it actually lead to 
         a well-mixed deck? That’s what we set out to explore. Before diving into the results, 
         let’s take a closer look at what these shuffle techniques are and how we can simulate them.
         ''')

st.subheader('Common Shuffling Tecniques', divider=True)

st.write('''
       Not all shuffles are created equal. Some are practical, some are flashy favorites of stage magicians, 
         and others… well, they mostly exist to test your patience. Depending on where you are or who you're playing with,
         you might hear different names for similar techniques. Still, some of the most commonly used methods are the 
         riffle shuffle, overhand shuffle, and Hindu shuffle. 
         Let’s break down how each one works, and how useful they really are for randomizing a deck.
''')


st.markdown('''
            #### Riffle shuffle
            ''')

st.write('''The riffle shuffle is one of the most effective and widely used techniques for randomizing a deck. 
         It works by splitting the deck into two roughly equal halves and interleaving the cards, releasing them alternately 
         from each hand. Below, you can see a gif demonstrating how it’s done. Notice how some people like to add a little 
         flair at the end? That move is called a *bridge finish*—also known as a *waterfall* or *cascade*. 
         It’s a stylish way to bring the cards neatly back together, but it doesn’t actually affect the order of the cards.''')

col = st.columns(3)[1]
col.image('https://fredhohman.com/card-shuffling/static/images/riffle.gif',width=300, caption='A popular riffle shuffle trick')

expander = st.expander("See mathematical modeling of riffle shuffle")
expander.markdown(r'''
         To model how a riffle shuffle randomizes a deck, we can turn to a classic statistical framework. 
         Back in the 1950s, mathematician Edgar Gilbert had a clever idea, which he developed with input from 
         Claude Shannon (yes, the father of information theory) and later refined by Jim Reeds. 
         Together, they laid the foundation for what’s now known as the ***Gilbert–Shannon–Reeds model*** (GSR model).

         The GSR model describes riffle shuffling as a two-stage, probability-driven process: the cutting stage and the riffling stage.
         First, the deck of n cards is split into two roughly equal packets containing $k$ and $(n-k)$ cards, where $k$ follows a 
            binomial distribution: $k\sim binomial(n,\frac{1}{2})$.
         Next, the cards are interleaved by choosing the next card from one of the two packets based on the number of cards remaining in each.
         When packets have $a$ and $b$ cards remaining, the next card comes 
         from packet A with probability $\frac {a}{a+b}$ and packet B with probability $\frac {b}{a+b}$. 
         These probabilities update dynamically after each card is dropped, simulating a realistic riffle shuffle. 
        ''')

expander.write(r'''
        The GSR model offers a simple yet accurate representation of riffle shuffles. While mathematicians favor its elegant 
        symmetry, simulations benefit from more flexible models with tunable parameters. Our implementation extends 
        the GSR framework with two key modifications:
        Instead of a binomial distribution with fixed parameters$\text{binomial}(n, \frac{1}{2})$, we parameterize the split using a 
         rounded normal distribution $\mathcal{N}(\mu, \sigma^2)$. 
        During card merging, rather than dropping single cards, we drop clumps of $X$ successive cards where
          $(X-1) \sim \text{Poisson}(\lambda)$. This $\lambda$-controlled clumping mimics observed human tendencies 
         where packets release card bursts rather than perfect singletons. 
        ''')

expander.write('''
    - When $\lambda=0$, it is a **GSR shuffle**.

    - When every card is perfectly interleaved without successive cards from the same packet, it is called a **Faro shuffle**. 
    
         Evidentally, this is an ineffective shuffle for randomization because only limited deck orders can be achieved and
        the deck returns to its initial state after certain sequences of Faro shuffles.

        ''')

st.markdown('#### Overhand Shuffle and Hindu Shuffle')
st.write('''
            The overhand shuffle is one of the most familiar and accessible shuffling methods. It works by repeatedly 
            transferring small blocks of cards from the top to the bottom of the deck, reversing the order of those blocks 
            along the way. While this process introduces some randomness, it tends to preserve the local structure of the 
            deck and requires many repetitions to achieve a well-mixed state. For this reason, it's often used in 
            combination with other techniques to improve overall effectiveness.
            ''')

col= st.columns(3)[1]
col.image('https://cdn.shopify.com/s/files/1/0481/4395/8177/files/how_to_shuffle_tarot_cards_overhand_shuffle_2_1024x1024.gif?v=1684300303',width=300,caption='Overhand shuffle')
st.write('''
        Closely related to the overhand shuffle is the Hindu shuffle—a favorite in many parts of Asia and a staple 
         in magic performances. Instead of pulling cards from the bottom like in the overhand, the Hindu shuffle lifts 
         a packet from the middle of the deck, and repeatly put a smaller packets of card from the packet on to the top of the deck.
         This method also tends to preserve clusters of cards, especially those near the bottom, which can be both a blessing for magicians 
         and a curse for randomness. Like the overhand, it introduces some disorder, but usually needs backup from other 
         shuffles to truly scramble the deck.
        ''')
col= st.columns(3)[1]
col.image('https://media1.tenor.com/m/QsJjX7uRGGoAAAAd/hindu-shuffle-world-xm.gif', width=300,caption='Hindu Shuffle')
st.markdown('''
            #### Other Shuffle Techniques
            ''')

st.write('''
        There are several simple yet commonly used techniques in card games and casinos, such as cutting. 
         A basic cut splits the deck into two parts and swaps them, while fancier versions like the Scarne 
         cut are more complex. Pile shuffling involves dealing cards into several stacks and then recombining them; 
         dealing cards in small batches is essentially a form of pile shuffling as well. Fancy tricks such as trip cuts or strip shuffles, 
         often seen in casinos, are essentially quick overhand and Hindu shuffles used between riffles to break up clumps. 
         We can also test whether these tricks actually make a difference in our experiments.
         ''')

st.subheader('How to evaluate the shuffle results',divider=True)
st.write('''
    Before diving into the deep water of defining metric for evaluation, I'd like to introduce a fascinating magic  trick 
    just to demonstrate how unreliable our preception of randomness is. The game is called *Premo* by American magician and
         mathematician Charles T. Jordan over 100 years ago and analyzed by Bayer and Diaconis in 1992. It, with a chance of 
         failing, can predict the card inserted at a random position after as many as 3 riffle shuffles and card cutting. 
''')

container = st.container(border=True)
container.markdown('##### ***Premo: The Magic Act***')
tab1, tab2, tab3, tab4 = container.tabs(["*Step 1*", "*Step 2*", "*Step 3*", "*Step 4*"])
with tab1:
    st.write('- **Prepare an unshuffled deck**')
    cards = list(range(52))
    
    styled_cards = [
    f"<span style='display: inline-block; font-size: 15px; background-color:#EBBEEB; padding: 3px 6px; margin: 3px 6px; border-radius: 8px;'>{card}</span>"
    for card in cards
    ]

    html = f"<div style='text-align: center;'>{''.join(styled_cards)}</div>"
    st.markdown(html, unsafe_allow_html=True)

with tab2:
    st.write(
        f"- **Without looking, have a spectator cut the deck, riffle shuffle it, cut it again, riffle shuffle once more, "
        f"and make a final cut. Take a look at the top card, in this case {cards[0]}**"
    )
    cards = functions.shuffling(cards, shuffle_proc=['cutting_shuffle','gsr','cutting_shuffle','gsr','cutting_shuffle'])
    
    styled_cards = [
        f"<span style='display: inline-block; font-size: 15px; "
        f"background-color: {'#FFCCCC' if i == 0 else '#EBBEEB'}; "
        f"padding: 3px 6px; margin: 3px 6px; border-radius: 8px;'>{card}</span>"
        for i, card in enumerate(cards)
    ]

    html = f"<div style='text-align: center;'>{''.join(styled_cards)}</div>"
    st.markdown(html, unsafe_allow_html=True)

with tab3:
    st.write('- **Insert the top card at a random position**')
    position = random.randint(1,len(cards)-1)
    cards = cards[1:position] + [cards[0]] + cards[position:]
    styled_cards = [
            f"<span style='display: inline-block; font-size: 15px; "
            f"background-color: {'#FFCCCC' if i == position -1 else '#EBBEEB'}; "
            f"padding: 3px 6px; margin: 3px 6px; border-radius: 8px;'>{card}</span>"
            for i, card in enumerate(cards)
        ]
    html = f"<div style='text-align: center;'>{''.join(styled_cards)}</div>"
    st.markdown(html, unsafe_allow_html=True)

with tab4:
    st.write('**Let the spectator do another cut and another riffle shuffle, then cut the deck again to let the card really hard'
    'to find.**')
    cards = functions.shuffling(cards, shuffle_proc=['cutting_shuffle','gsr','cutting_shuffle'])

    styled_cards = [
        f"<span style='display: inline-block; font-size: 15px; "
        f"background-color: #EBBEEB; "
        f"padding: 3px 6px; margin: 3px 6px; border-radius: 8px;'>{card}</span>"
        for i, card in enumerate(cards)
    ]

    html = f"<div style='text-align: center;'>{''.join(styled_cards)}</div>"
    st.markdown(html, unsafe_allow_html=True)

container.write('')
container.write('')
with container.expander('**Magician\'s act**'):
    
    st.write('After staring at the face and values of the deck for 2 minutes, the magician make a guess:')
    st.write('I think the card is: ', functions.winding_num(cards).index(max(functions.winding_num(cards))))

    # col1, col2 =st.columns([1,4])
    st.write('Not correct?')
    st.button('Let\'s try again', type='primary')
container.write(''' 
         The guess is made by calculating a measure called the *winding number*. As the guess is correct only about half of
         the time, there are
         improved versions of this act. You can read more about the magic and the math behind it on 
         [this site](https://sites.google.com/site/erfarmer/premo-card-trick) or 
         [this paper](https://www.stat.berkeley.edu/~aldous/157/Papers/bayer_diaconis.pdf).
''')

st.write(r'''
        As presented by the magic trick above, randomness is always a tricky concept for humans to fully grasp. 
         After 3 shuffles, the deck seems very random, but we can still discover some patterns and guess a card with a
         half-half persentage. So, how can we tell if a deck is truly well shuffled 
         and randomized? While there are rigorous mathematical approaches to this question, we explore two more 
         intuitive paths here.

        - First, we sidestep the abstract nature of randomness and focus on a more practical measure: how different the 
         hands are between consecutive rounds. Intuitively, a well-shuffled deck should produce hands that look completely 
         unrelated to the previous ones. To quantify this, we introduce a *well-shuffleness* score based on **Jaccard 
         similarity**, which evaluates the maximum similarity between hands. This approach works well for casual or friendly 
         games, although—\*fair warning\*—it might leave room for subtle cheating if someone’s really clever about it.

        - Second, we tackle the randomness question head-on with a card guessing game. D. Bayer AND P. Diaconis proposed 
         a distance to measure the randomness, let's call it **D-B Distance**. The idea is simple: make educated 
         guesses for each card in the shuffled deck, one by one, based on the knowledge of the original unshuffled order and 
         the cards already revealed. The total number of correct guesses $Y$ can act as a randomness indicator. 
         For a well-shuffled 52-card deck, the expected number of correct guesses
        $        E(Y) = \frac{1}{52} + \frac{1}{51} + \cdots + \frac{1}{1} \approx 4.54$.
        More generally, with $n$ cards, the number of correct guesses follows an approximately normal distribution with 
         mean and variance of $\log n$. This method makes it harder to cheat and provides a stricter measurement 
         for settings like casinos.
''')

st.subheader('Simulating Shuffles',divider=True)
st.write('Alright, let\'s now try to answer the questions asked with the foundation we have built.')

st.markdown('#### How many riffle shuffle can mix a deck?')

st.write('''
    We simulate 100 riffle shuffle sequences using the Gilbert–Shannon–Reeds (GSR) model, 
         where each sequence consists of multiple consecutive GSR shuffles applied to a standard deck of cards. 
         By analyzing the distribution and randomness of the deck after each shuffle, we quantitatively assess 
         how effectively the GSR model mixes the cards over time.

    Using two custom metrics, we perform statistical tests to compare the shuffled deck against a truly random deck, 
         examining differences in their means and overall distributions. The tests include the Two-sample t-test, 
         Kolmogorov–Smirnov test, and one-sided Mann–Whitney U test. Our conclusions are as follows:

    - Jaccard metric: Approximately 3–4 consecutive GSR shuffles suffice to make the deck significantly different from 
         its initial order, with p-values exceeding 0.05. However, it is noteworthy that occasionally, additional shuffles 
         can cause a slight increase in similarity to the previous arrangement.

    - DB distance metric: About 7 shuffles are required to achieve a fully randomized deck where prior knowledge of the 
         deck order does not aid in predicting the current order. This result aligns well with the mathematical proof by 
         Bayer and Diaconis. Combined with the previous observation, it suggests that even after perfect shuffling, 
         some hands may remain surprisingly similar to prior ones.

    Below is the distribution of the DB distance after each shuffle compared to a random deck. Notice how there is a
         cut off at around 3 shuffles. This sugguest that even though the deck is not strictly random, 3-4 shuffles are
         almost good enough. But off course, this is consecutive shuffles without cutting or other shuffles involved;
         it is also GSR that maybe not everyone is able to do perfectly.


''')


button = st.button('start simulation')
if button:
    with st.spinner("Simulating shuffling...", show_time=True): 
        result = functions.compare2strategy(cards, simulation_time = 100, max_shuffle = 10, shuffle_proc=['gsr'],
                    shuffle_par = {'riffle_shuffle': {'deviding_p': 0.5, 'var': 1, 'shuffling_lam': 1, 'time': 1}},
                    dealing_par = {'players': 3, 'chunk_size': 17}, metrics=['jaccard','dice','mcgrath_guesses'])



    with st.spinner("Generating image...", show_time=True): 


        # Sort the types in the desired top-to-bottom order
        types = list(result.type.unique())[::-1]  # Reverse the order
        data = [result[(result.metric == 'mcgrath_guesses') & (result.type == col)].value for col in types]

        colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', len(types), colortype='rgb')

        fig = go.Figure()

        # Add violins (rendered bottom-up, so reverse to get top-to-bottom order)
        for data_line, color, label in zip(data, colors, types):
            fig.add_trace(go.Violin(
                x=data_line,
                y=[label] * len(data_line),  # Assign y label to each point
                line_color=color,
                name=label,
                orientation='h',
                side='positive',
                width=3,
                points=False,
                showlegend=False
            ))

        # Customize layout
        fig.update_layout(
            width=1000,
            height=200 + 30 * len(types),  # Dynamic height based on number of types
            title="",
            xaxis_title="DB Distance",
            yaxis_title="Shuffles",
            font=dict(family="Arial", size=14, color="black"),
            xaxis=dict(range=[-2,48], showgrid=False, zeroline=False),  # Reverse x-axis
            yaxis=dict(categoryorder='array', categoryarray=types)  # Preserve top-to-bottom order
        )

        st.plotly_chart(fig, use_container_width=True)


st.write('')
st.write('')
st.write('')
st.markdown('#### Is an amateur riffle shuffle different?')
st.markdown('''
We also looked at a more “amateur” riffle shuffle, where instead of dropping one card at a time, the shuffler tends to drop 
several cards in a row — modeled by a Poisson distribution.

**What we found:**

- Amateur shuffles need more repetitions to mix well.
- The bigger the batches of cards dropped, the more shuffles it takes to get random.
    - After just 1 or 2 shuffles, the deck’s randomness (measured by DB distance) shows much higher variance than a perfect GSR shuffle.
    - But after 3–4 shuffles, things start to settle.
    - About **15 shuffles** are needed if cards drop with $Poisson(1.5)$, and over **20 shuffles** if $Poisson(3)$.
- How you cut the deck and how consistently you split it also matters — it can reduce the number of shuffles needed.

So, being a bit amateur doesn’t change much — just make sure to cut consistently and try to minimize chunks of cards droped at once.
''')

st.markdown('#### What is a good shuffling strategy?')

st.write('There are so many shuffling techniques that have not being tested, such as cutting and pile\'s shuffles. These' \
'are good techniques that works well in combination with other techniques. Below is a table created by Bayer and Diaconis to demonstrate how cutting' \
'works together with riffles shuffles by the average number of correct guesses in 100,000 simulations. ' \
'To test how your strategy work let\'s build a interactive interface.')

st.image('images/cutting.png',width=1000)

options = ['Riffle shuffle','Overhand Shuffle','Hindu Shuffle','Cutting the Deck','GSR']


with st.container(border=True):
    st.markdown('#### **Simulate your shuffle**')
    n_shuffles = st.slider("How many shuffles are you doing?", 1, 6, 3)

    my_shuffles = []
    number = ['1st', '2nd','3rd', '4th', '5th']
    for i in range(n_shuffles):
        shuffle = st.pills(
            f'   *{i+1}*.  What is your {number[i]} shuffle?',
            options,
            selection_mode="single",
            key=f'shuffle_{i}'
        )
        my_shuffles.append(shuffle)  # Or append if you want list of lists
    st.write(f' {n_shuffles+2} . At the dealing process:')
    if st.toggle("Add a pile shuffle at the dealing process."):
        my_shuffles.append('Pile Shuffle')

    st.write("**Your shuffle process is:**")




    text = f'<i><b>{my_shuffles[0]}</b></i>'
    for i in range(1, len(my_shuffles)):
        text += f'  &rarr;  &nbsp; <i><b>{my_shuffles[i]}</b></i> &nbsp;'
    
    st.markdown(
        f'''<div style='background-color: #f0f2f6; padding: 10px; border-radius: 10px; line-height: 1; display:inline-block;''>
                {text}
            </div>''',
        unsafe_allow_html=True
    )



    
    st.write('')
    st.divider()
    st.write('**Now let\'s set the parameters of the shuffles:**')

    my_shuffles_set = set(my_shuffles)
    shuffling_par_dict = {}
    dealing_par = {}
    for shuffle in my_shuffles_set:
        if shuffle != "GSR" and shuffle is not None:
            st.markdown(f'- **In your {shuffle}:**')
        

        if shuffle == 'Riffle shuffle':
            col1, col2, col3 = st.columns(3)
            deviding_p = col1.slider(
                "How close to the center do you typically split the deck when starting the riffle shuffle?",
                0.0, 1.0, 0.5, key=f'{shuffle}_deviding_p'
            )
            var = col2.slider(
                "How much variation is there in where you cut the deck (higher = less precise)?",
                0, 36, 1, key=f'{shuffle}_var'
            )
            shuffling_lam = col3.slider(
                "How many interleaving batches (on average) do you create during the riffle? (Poisson λ)",
                0.0, 5.0, 1.0, key=f'{shuffle}_lambda'
            )
            shuffling_par_dict['riffle_shuffle'] = {
                'deviding_p': deviding_p,
                'var': var,
                'shuffling_lam': shuffling_lam,
                'time': 1
            }

        if shuffle == 'Overhand Shuffle':
            col1, col2 = st.columns(2)

            var = col1.slider(
                "What is the variance in the size of each packet you drop?",
                0, 16, 1, key=f'{shuffle}_var'
            )
            overhand_time = col2.slider(
                "How many times do you cut the deck per shuffle?",
                1, 12, 5, key=f'{shuffle}_time'
            )
            shuffling_par_dict['overhand_shuffle'] = {
                'var': var,
                'overhand_time': overhand_time,
                'time': 1
            }

        if shuffle == 'Hindu Shuffle':
            col1, col2, col3,col4 = st.columns(4)

            location = col1.slider(
                "Where in the deck do you pull cards from? (0 = top, 1 = bottom)",
                0.0, 1.0, 0.5, key=f'{shuffle}_location'
            )
            prop = col2.slider(
                "What proportion of the deck size do you expect to pull as a packet?",
                1, 12, 5, key=f'{shuffle}_prop'
            )
            var = col3.slider(
                "What is the variance in the size of the packet you pull?",
                0, 16, 1, key=f'{shuffle}_var'
            )

            time = col4.slider(
                "How many times do you cut the packet after you pull it out?",
                0, 16, 1, key=f'{shuffle}_time'
            )

            shuffling_par_dict['hindu_shuffle'] = {
                'location': location,
                'prop': prop,
                'var': var,
                'time': time
            }

        if shuffle == 'Cutting the Deck':
            col1, col2 = st.columns(2)

            location = col1.slider(
                "At what position in the deck do you make the cut? ",
                0.0, 1.0, 0.5, key=f'{shuffle}_location'
            )
            var = col2.slider(
                "How much variation is there in your cut location?",
                0, 16, 1, key=f'{shuffle}_var'
            )

            shuffling_par_dict['cutting_shuffle'] = {
                'location': location,
                'var': var
            }


        if shuffle == 'Pile Shuffle':
            col1, col2 = st.columns(2)

            players = col1.slider(
                "How many piles are you diving the deck? ",
                1, 10, 3, key=f'{shuffle}_location'
            )
            chunk_size = col2.slider(
                "How much cards are each pile getting each time?",
                1, int(52/players), 3, key=f'{shuffle}_var'
            )

            dealing_par = {
                'players': players,
                'chunk_size': chunk_size
            }


    rename_myshuffles_dict = {
    'Riffle shuffle': 'riffle_shuffle',
    'Overhand Shuffle': 'overhand_shuffle',
    'Hindu Shuffle':'hindu_shuffle',
    'Cutting the Deck':'cutting_shuffle',
    'GSR':'gsr'
    }


    my_shuffle_proc = [rename_myshuffles_dict.get(shuffle, shuffle) for shuffle in my_shuffles]


    st.write('')
    st.write('')
    col = st.columns(3)[1]
    
    button = col.button('Simulate the shuffle', type='primary')
    st.write('')


    with st.spinner("Evaluating shuffles...", show_time=True):
        if button and None in my_shuffles:
            st.markdown("<span style='color:red'><i>You haven't finished defining the shuffle process.</i></span>", unsafe_allow_html=True)

        elif button:
            cards=list(range(52))
            result = functions.compare2random(cards, simulation_time = 1, simulation_time_random = 100, max_shuffle = 10, 
                                    shuffle_proc = [shuffle for shuffle in my_shuffle_proc if shuffle != 'Pile Shuffle'],
                                    shuffle_par = shuffling_par_dict,
                                    dealing_par = dealing_par , metrics=['jaccard','dice','mcgrath_guesses'])
            print(functions.compare2random(cards, simulation_time = 1, simulation_time_random = 100, max_shuffle = 10, 
                                    shuffle_proc = [shuffle for shuffle in my_shuffle_proc if shuffle != 'Pile Shuffle'],
                                    shuffle_par = shuffling_par_dict,
                                    dealing_par = dealing_par , metrics=['jaccard','dice','mcgrath_guesses']))
            # st.dataframe(result)

            tab1, tab2 = st.tabs(['Jaccard','DB Distance'])
            
            
            with tab1:
                # Data
                random_values = result[(result.type == 'Random') & (result.metric == 'jaccard')]['value']
                shuffled_value = result[(result.type == 'Shuffled') & (result.metric == 'jaccard')]['value'].values[0]

                st.write(f"***Your shuffle is more effective than {len(result[(result.type == 'Random') & (result.metric == 'jaccard') & (result.value>shuffled_value)]):.1f}% of the random shuffle.***")

                if len(result[(result.type == 'Random') & (result.metric == 'jaccard') & (result.value>shuffled_value)])>5:
                    st.write('***Your shuffle can be effective in making sure distinction before previous hands***')
                else:
                    st.write('***Your shuffle may not cause clear distinction before previous hands***')        

                # st.write(random_values)
                # KDE calculation
                kde = gaussian_kde(random_values, bw_method=.5/ random_values.std(ddof=1)) 
                x_vals = np.linspace(0, 1, 500)
                y_vals = kde(x_vals)

                # Create plot
                fig = go.Figure()

                # KDE curve with fill
                fig.add_trace(go.Scatter(
                    x=x_vals, y=y_vals,
                    mode='lines',
                    fill='tozeroy',
                    name='Random KDE',
                    line=dict(color='skyblue'),
                    showlegend=False
                ))

                # Mark shuffled value with vertical line
                fig.add_trace(go.Scatter(
                    x=[shuffled_value, shuffled_value],
                    y=[0,y_vals[np.argmin(np.abs(x_vals - shuffled_value))]],
                    mode='lines',
                    line=dict(color='crimson', dash='dash'),
                    name='Your shuffle',
                    showlegend=False
                ))

                # Add marker on the KDE curve at shuffled_value
                shuffled_y = kde(shuffled_value)
                fig.add_trace(go.Scatter(
                    x=[shuffled_value,shuffled_value],
                    y=[y_vals[np.argmin(np.abs(x_vals - shuffled_value))]],
                    mode='markers+text',
                    marker=dict(
                        color='crimson',
                        size=12,
                        line=dict(color='black', width=1.5)
                    ),
                    text=["Your shuffle"],
                    textposition="top center",
                    textfont=dict(size=18, color='crimson'),
                    showlegend=False
                ))


                # Layout
                fig.update_layout(
                    title="",
                    xaxis_title="Jaccard",
                    yaxis_title="Density",
                    template="simple_white",
                    width=800,
                    height=500,
                    xaxis=dict(showgrid=False, zeroline=False, showline=False),
                    yaxis=dict(showgrid=False, showline=False),
                    
                )

                st.plotly_chart(fig, use_container_width=True)




            with tab2:
                # Data
                random_values = result[(result.type == 'Random') & (result.metric == 'mcgrath_guesses')]['value']
                shuffled_value = result[(result.type == 'Shuffled') & (result.metric == 'mcgrath_guesses')]['value'].values[0]

                st.write(f"***Your shuffle is more effective than {len(result[(result.type == 'Random') & (result.metric == 'mcgrath_guesses') & (result.value>shuffled_value)]):.1f}% of the random shuffle.***")

                if len(result[(result.type == 'Random') & (result.metric == 'mcgrath_guesses') & (result.value>shuffled_value)])>5:
                    st.write('***Your shuffle can be effective***')
                else:
                    st.write('***Your shuffle may not reach perfect randomness***')        


                # KDE calculation
                kde = gaussian_kde(random_values, bw_method=1.5 / random_values.std(ddof=1))
                x_vals = np.linspace(random_values.min() - 1, random_values.max() + 1, 500)
                y_vals = kde(x_vals)

                # Create plot
                fig = go.Figure()

                # KDE curve with fill
                fig.add_trace(go.Scatter(
                    x=x_vals, y=y_vals,
                    mode='lines',
                    fill='tozeroy',
                    name='Random KDE',
                    line=dict(color='skyblue'),
                    showlegend=False
                ))

                # Mark shuffled value with vertical line
                fig.add_trace(go.Scatter(
                    x=[shuffled_value, shuffled_value],
                    y=[0,y_vals[np.argmin(np.abs(x_vals - shuffled_value))]],
                    mode='lines',
                    line=dict(color='crimson', dash='dash'),
                    name='Your shuffle',
                    showlegend=False
                ))

                # Add marker on the KDE curve at shuffled_value
                shuffled_y = kde(shuffled_value)
                fig.add_trace(go.Scatter(
                    x=[shuffled_value,shuffled_value],
                    y=[y_vals[np.argmin(np.abs(x_vals - shuffled_value))]],
                    mode='markers+text',
                    marker=dict(
                        color='crimson',
                        size=12,
                        line=dict(color='black', width=1.5)
                    ),
                    text=["Your shuffle"],
                    textposition="top center",
                    textfont=dict(size=18, color='crimson'),
                    showlegend=False
                ))


                # Layout
                fig.update_layout(
                    title="",
                    xaxis_title="DB Distance",
                    yaxis_title="Density",
                    template="simple_white",
                    width=800,
                    height=500,
                    xaxis=dict(showgrid=False, zeroline=False, showline=False),
                    yaxis=dict(showgrid=False, showline=False),
                    
                )

                st.plotly_chart(fig, use_container_width=True)

st.write('As it turns out, the routine I always use presented in the start is not that good both in terms of creating different hands and randomize the' \
'deck. However, if I try to increase the quality of the shuffle or add a pile shuffle at the end, it is suddenly decent in both' \
'perspective. How does your shuffling routine do compared to total randomized cards?')


st.subheader('I learned this today...', divider=True)
st.write('''
The shuffling is fun and everything, but it is hard to have an intuitive understanding of it. If I have to say I learned anything
         other than the magic tricks and statistical models after all this, I have to say I only learned that it is really hard to
         reach the state that statisticians call random compared to our intuition. 
         
         
Human beings have wrestled with randomness for millennia. We want our arrows to fly straight, unbothered by turbulence; 
         we want to predict the weather without too much uncertainty; and we want our futures to be clear and calculable. 
         Yet somewhere along the way, we realized we could also be friend with randomness: to flip a coin and settle disputes, 
         to design games whose outcomes no one can foresee, and here in this piece, to shuffle cards and create fair play.

But here's the twist: even our tools of randomness are only as fair as we are fallible. Skilled hands can flip a coin and 
         make it land the way they want. A perfectly executed card shuffle isn’t random at all — in fact, the entire point 
         of shuffling is that we’re bad at doing it perfectly. 

Our love-hate relationship with randomness continues, but our understanding has grown sharper. As it turns out, we humans are very
         bad at generating or reconising random things. Here is an example in the figure below. Some random processes follow 
         surprising patterns; others resist any kind of prediction we have. Is there such a thing as true randomness — something 
         completely without structure? Or is everything, in principle, deterministic, just waiting for a more precise model?
''')


col = st.columns([2,8,1])[1]
col.image('https://i.redd.it/w4gz0wzz1i821.png',width=400)


st.write('''
But maybe that’s not the point. Maybe randomness is less about cosmic uncertainty and more about us — our limits, 
         our clever workarounds, and our desire to be surprised. After all, we shuffle not to reach chaos, but to escape 
         control. And in that brief moment when no one knows what card comes next, randomness feels real enough.


''')