
require( ['ToledoChess'], function(ToledoChess){

	window.OnClick = OnClick;

	var ai = ToledoChess;
	ai.drawCallback = DrawPieces;
	ai.aiCallback = aiCallback;

	CreateChessboardView();
	DrawPieces();

	function aiCallback( player, from, to)
	{
		console.log( player, from, to);
	}

	function CreateChessboardView() {
		var x, y, i;
		var a = "<table cellspacing=0 align=center>";
		for (y=0; y<8; y++) {
			a += "<tr>";
			for (x=0; x<8; x++) {
				i = y*10 + x + 21;
				a += "<th width=60 height=60 onclick=OnClick(" + i + ") id=o" + i +
					 " style='line-height:50px;font-size:50px;border:2px solid #dde' bgcolor=#" +
					 (((x+y) & 1) ? "c0c0f0>" : "f0f0f0>");
			}
			a += "</tr>";
		}
		a += "<tr><th colspan=8><select id=t style='font-size:20px'>";
		a += "<option>&#9819;<option>&#9820;<option>&#9821;<option>&#9822;";
		a += "</select></tr></table>";
		document.write(a);
	}

	function DrawPieces() {
		console.log('DrawPieces');
		var pieces = "\xa0\u265f\u265a\u265e\u265d\u265c\u265b  \u2659\u2654\u2658\u2657\u2656\u2655";
		var p, q;
		for (p=21; p<99; ++p) {
			if (q = document.getElementById("o" + p)) {
				q.innerHTML = pieces.charAt(ai.board[p] & 15);
				q.style.borderColor = (p == ai.getMoveFrom()) ? "red" : "#dde";
			}
		}
	}
	
	function OnClick(fieldID) {
		ai.OnClick(fieldID);
	}


});