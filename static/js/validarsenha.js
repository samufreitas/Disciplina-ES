// validarSenha.js
function validarSenha() {
    var password = document.getElementById("senha").value;
    var nome = document.getElementById("first_name").value;
    var sobrenome = document.getElementById("last_name").value;
    var email = document.getElementById("email").value;

    // Verifica se a senha possui pelo menos 8 caracteres
    if (password.length < 8) {
        alert("Sua senha precisa ter pelo menos 8 caracteres.");
        return false;
    }

    // Verifica se a senha contém informações pessoais
    if (password.includes(nome) || password.includes(sobrenome) || password.includes(email)) {
        alert("Sua senha não pode ser muito parecida com o resto das suas informações pessoais.");
        return false;
    }

    // Verifica se a senha é comumente utilizada
    var senhasComuns = ["123456", "password", "senha123"]; // Lista de senhas comuns
    if (senhasComuns.includes(senha.toLowerCase())) {
        alert("Sua senha não pode ser uma senha comumente utilizada.");
        return false;
    }

    // Verifica se a senha é inteiramente numérica
    if (!isNaN(password)) {
        alert("Sua senha não pode ser inteiramente numérica.");
        return false;
    }

    return true;
}

function validarMatricula() {
            var matricula = document.getElementById("username").value;
            var pattern = /^[0-9]{8,}$/;
            if (!pattern.test(matricula)) {
                alert("A matrícula deve conter no mínimo 8 dígitos numéricos.");
                return false;
            }
            return true;
        }