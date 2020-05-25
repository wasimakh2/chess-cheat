def shortenFEN(fen):
	return fen.replace('11111111','8').replace('1111111','7') \
			.replace('111111','6').replace('11111','5') \
			.replace('1111','4').replace('111','3').replace('11','2')

def lengthenFEN(fen):
	return fen.replace('8','11111111').replace('7','1111111') \
			.replace('6','111111').replace('5','11111') \
			.replace('4','1111').replace('3','111').replace('2','11')

def unflipFEN(fen):
	if len(fen) < 71:
		fen = lengthenFEN(FEN)
	return '/'.join([ r[::-1] for r in fen.split('/') ][::-1])

def getCastlingStatus(fen):
	fen = lengthenFEN(fen)
	status = ['','','','']
	if fen[4] == 'k':
		if fen[0] == 'r':
			status[3] = 'q'
		if fen[7] == 'r':
			status[2] = 'k'
	if fen[63+4] == 'K':
		if fen[63+0] == 'R':
			status[1] = 'Q'
		if fen[63+7] == 'R':
			status[0] = 'K'
	status = ''.join(status)
	return status if status else '-'
