// ******************** Дебаггинг вызовы функций ********************

var DBG_CALLS_CNT = 0;
var DBG_ON = true;
// DBG_ON = false;

// Добавить количество пробелов равное глобальной переменной CALLS_CNT
function dbgSpaces() {
    var out = '';
    for(var i = 0; i < DBG_CALLS_CNT; i++) {
	out += '....';
    }
    return(out);
}

// Напечатать имя вызываемой функции
// с лидирующими пробелами соответстующими глубине стека вызовов
function dbgFuncCall(name) {
    if(DBG_ON) {
	var out = dbgSpaces() + name;
	DBG_CALLS_CNT++;
	console.log(out);
    }
}

// Уменьшить на 1 счетчик стека вызовов
function dbgFuncReturn() {
    if(DBG_ON) {
	DBG_CALLS_CNT--;
    }
}

// Печать в косоль FireBug. Включается/выключается глобальной
// переменной DBG_ON
// ---
// Parameters:
function dbgConsole() {
    if(DBG_ON) {
	out = '';
	for(var i = 0; i < dbgConsole.arguments.length; i++) {
	    out += dbgConsole.arguments[i] + ' ';
	}
	console.log(out);
    }
}

//
// ---
// Parameters:
function dbgButton() {
    if(DBG_ON) {
	var out ='<button id="debug_button">Debug button</button>';
	$('#container').prepend(out);
	$('#debug_button').click(
	    function(){
		treeRegionBranchByCodeGetAndDraw('4.4.1','en');
	    });
    }
    return;
}


// ******************** Дебаггинг json ********************

// Распечатать на консоль словарь "json.query"
// ---
// Parameters:
function dbgJsonQueryPrint(json) {
    if(DBG_ON) {
	dbgFuncCall('dbgJsonQueryPrint');
	for(var k in json.query) {
	    console.log(k,'\t = ',json.query[k]);
	}
	dbgFuncReturn();
    }
}

// Печать в косоль FireBug. Не Включается/выключается глобальной
// переменной DBG_ON Применяется, когда не нужен весь стек
// ---
// Parameters:
function dbgConsoleDirect() {
    out = '';
    for(var i = 0; i < dbgConsoleDirect.arguments.length; i++) {
	out += dbgConsoleDirect.arguments[i] + ' ';
    }
    console.log(out);
}
