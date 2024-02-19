uint constant VAR0 = 12;
contract CONT1 {
address public VAR1;
function CONT1() public {
VAR1 = msg.sender;
}
modifier MOD1() {
require(msg.sender == VAR1);
_;
}
function FUN2(address VAR2) public MOD1 {
require(VAR2 != address(0));
VAR1 = VAR2;
}
}
contract CONT2 is CONT1 {
address public VAR3;
modifier MOD2() {
require(msg.sender == VAR3);
_;
}
function FUN3(address VAR4) public MOD1 {
VAR3 = VAR4;
}
function FUN4() public MOD2 {
VAR1 = VAR3;
VAR3 = address(0);
}
}
contract CONT3 is CONT2 {
bool public VAR5 = false;
string public VAR6;
function FUN5(bool VAR7, string VAR8) public MOD1 {
VAR5 = VAR7;
VAR6 = VAR8;
}
}