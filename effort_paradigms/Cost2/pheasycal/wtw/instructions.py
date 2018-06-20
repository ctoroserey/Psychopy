
# present pre-block task instructions and demo trials
# the contents of the instructions depend on the block number and
# the response requirements.

from __future__ import division
import wtw
import wtw.drawSample

##################################################
# main function to present a block of instructions
def instrucBlock(blockParams, stimObjects, thisExp, expObjects):

    # unpack inputs
    win = expObjects['win']
    message = stimObjects['message']

    # set the text for the 5 instructions screens
    # depending on both the block number and the response function
    # ASSUME for now there are 2 blocks w/ different response reqs.
    instrucScreenText = setInstrucScreenText(blockParams)

    # custom parameters for demo trials
    blockParamsDemo = blockParams.copy()
    blockParamsDemo['trialLimit'] = 1 # will present only 1 trial
    blockParamsDemo['drawSample'] = wtw.drawSample.fixed10 # with a fixed 10 s delay
    blockParamsDemo['totalEarned'] = 0 # 2nd practice block earnings start from zero

    # present interleaved text screens and demo trials
    for i in range(4):
        wtw.showMessage(win,message,instrucScreenText[i])
        wtw.showTrials(blockParamsDemo, stimObjects, thisExp, expObjects)

    # final text screen
    wtw.showMessage(win,message,instrucScreenText[4])


def setInstrucScreenText(blockParams):

    blockIdx = blockParams['blockIdx']
    responseFx = blockParams['checkSellResponse']
    blockDuration = blockParams['blockDuration']
    rwdLo = blockParams['rwdLo']
    rwdHi = blockParams['rwdHi']
    rwdUnit = blockParams['rwdUnit']

    # translate rwdUnit into currency ("cents" -> "money")
    if rwdUnit == u'\xa2':
        rwdCurrency = "money"
    elif rwdUnit == "pts":
        rwdCurrency = "points"
    else:
        raise Exception('Unexpected value for rwdUnit.')

    # initialize
    instrucScreenText = [None] * 5

    # some screens are the same for all conditions.
    # screen 1
    instrucScreenText[1] = "Good. Let's do it again. Wait until the token matures, then sell it."
    # screen 3
    instrucScreenText[3] = "Good. Let's do it again. Practice selling the token before it matures."

    # first block, squeeze to quit
    if blockIdx==0 and responseFx==wtw.detectResponse.squeezeHandGrip:
        # screen 0
        instrucScreenText[0] = 'You will see a token on the screen. '           +\
        'Tokens can be sold for %s. ' %(rwdCurrency)                            +\
        'Each token is worth %d%s at first. ' %(rwdLo, rwdUnit)                 +\
        'After some time, the token will "mature" and be worth more.\n\n'       +\
        'Now try a practice round. '                                            +\
        'Wait until the token matures, then squeeze the hand-grip to sell it.'
        # screen 1 is the same for all conditions
        # screen 2
        instrucScreenText[2] = 'You will have a limited amount of time to play. ' +\
        'If a token is taking too long, you might want to sell it '             +\
        'before it matures in order to move on to a new one.\n\n'               +\
        'Next, practice selling the token before it matures.'
        # screen 3 is the same for all conditions
        # screen 4
        paymentText = ''
        if rwdCurrency == 'money':
            paymentText = 'At the end of the experiment you will be paid '      +\
            'what you earned, rounded to the next 25 cents. '
        instrucScreenText[4] = 'In the first block you will have %d minutes to play. ' %(blockDuration/60) +\
        'Your goal is to earn the most %s you can in the available time.\n\n' %(rwdCurrency) +\
        paymentText + 'You should sell tokens quickly when they mature, '       +\
        'since their value will not change again.\n\n'                          +\
        'Any questions?'

    # first block, release to quit
    if blockIdx==0 and responseFx==wtw.detectResponse.releaseHandGrip:
        # screen 0
        instrucScreenText[0] = 'You will see a token on the screen. '           +\
        'Tokens can be sold for %s. ' %(rwdCurrency)                            +\
        'Each token is worth %d%s at first. ' %(rwdLo, rwdUnit)                 +\
        'You can increase its value by continuously squeezing the hand-grip. '  +\
        'After some time, the token will "mature" and be worth more.\n\n'       +\
        'Now try a practice round. '                                            +\
        'Squeeze the hand-grip until the token matures, then release the hand-grip to sell it.'
        # screen 1 is the same for all conditions
        # screen 2
        instrucScreenText[2] = 'You will have a limited amount of time to play. ' +\
        'If a token is taking too long, you might want to sell it '             +\
        'before it matures in order to move on to a new one.\n\n'               +\
        'Next, practice selling the token before it matures.'
        # screen 3 is the same for all conditions
        # screen 4
        paymentText = ''
        if rwdCurrency == 'money':
            paymentText = 'At the end of the experiment you will be paid '      +\
            'what you earned, rounded to the next 25 cents. '
        instrucScreenText[4] = 'In the first block you will have %d minutes to play. ' %(blockDuration/60) +\
        'Your goal is to earn the most %s you can in the available time.\n\n' %(rwdCurrency) +\
        paymentText + 'You should sell tokens quickly when they mature, '       +\
        'since their value will not change again.\n\n'                          +\
        'Any questions?'

    # second block, squeeze to quit
    if blockIdx==1 and responseFx==wtw.detectResponse.squeezeHandGrip:
        # screen 0
        instrucScreenText[0] = 'In the next block, instead of '                 +\
        'continuously squeezing the hand-grip you will just need to wait. '     +\
        'The token will mature after some amount of time.\n\n'                  +\
        'Try a practice round. '                                                +\
        'Wait until the token matures, then squeeze the hand-grip to sell it.'
        # screen 1 is the same for all conditions
        # screen 2
        instrucScreenText[2] = 'Like before, you can sell the token before '    +\
        'it matures if you think it is taking too long. '                       +\
        'Next, practice selling the token before it matures.'
        # screen 3 is the same for all conditions
        # screen 4
        instrucScreenText[4] = 'You will have %d minutes to play. ' %(blockDuration/60) +\
        'Like before, your goal is to earn the most %s you can in the available time.\n\n' %(rwdCurrency) +\
        'Any questions?'

    # second block, release to quit
    if blockIdx==1 and responseFx==wtw.detectResponse.releaseHandGrip:
        # screen 0
        instrucScreenText[0] = 'In the next block, instead of '                 +\
        'just waiting, you will need to squeeze the hand-grip continuously. '   +\
        'If you keep squeezing, the token will mature after some amount of time.\n\n' +\
        'Try a practice round. '                                                +\
        'Squeeze the hand-grip until the token matures, then release the hand-grip to sell it.'
        # screen 1 is the same for all conditions
        # screen 2
        instrucScreenText[2] = 'Like before, you can sell the token before '    +\
        'it matures if you think it is taking too long. '                       +\
        'Next, practice selling the token before it matures.'
        # screen 3 is the same for all conditions
        # screen 4
        instrucScreenText[4] = 'You will have %d minutes to play. ' %(blockDuration/60) +\
        'Like before, your goal is to earn the most %s you can in the available time.\n\n' %(rwdCurrency) +\
        'Any questions?'


    return instrucScreenText
