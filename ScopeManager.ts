import * as fs from "fs";

class ScopeManager {
  regex_whitespace: string;
  regex_number: string;
  regex_variable_number: string;
  regex_string: string;
  regex_variable_string: string;
  regex_variable: string;
  regex_print: string;
  regex_declared_number: string;
  regex_undeclared_number: string;
  regex_declared_string: string;
  regex_undeclared_string: string;
  scopes: any[][];
  block_identifiers: string[];

  constructor() {
    this.regex_whitespace = "\\s+";
    this.regex_number = "[+-]?\\d+(\\.\\d+)?";
    this.regex_variable_number =
      "[a-zA-Z_][a-zA-Z0-9_]*\\s*=\\s*" + this.regex_number;
    this.regex_string = '"([^"]*)"';
    this.regex_variable_string =
      "[a-zA-Z_][a-zA-Z0-9_]*\\s*=\\s*" + this.regex_string;
    this.regex_variable =
      "[a-zA-Z_][a-zA-Z0-9_]*\\s*=\\s*[a-zA-Z_][a-zA-Z0-9_]*";
    this.regex_print = "PRINT\\s+[a-zA-Z_][a-zA-Z0-9_]*";
    this.regex_declared_number = `NUMERO${this.regex_whitespace}${this.regex_variable_number}`;
    this.regex_undeclared_number = "NUMERO\\s+[a-zA-Z_][a-zA-Z0-9_]*";
    this.regex_declared_string = `CADEIA${this.regex_whitespace}${this.regex_variable_string}`;
    this.regex_undeclared_string = "CADEIA\\s+[a-zA-Z_][a-zA-Z0-9_]*";

    this.scopes = [];
    this.block_identifiers = [];
  }

  getTokenByIdentifier(identifier: string): any[] | null {
    for (const scope of this.scopes.slice().reverse()) {
      for (const currentToken of scope) {
        if (currentToken[2] === identifier) {
          return currentToken;
        }
      }
    }
    return null;
  }

  variableExists(identifier: string, scope: any[]): boolean {
    return scope.some((currentToken) => currentToken[2] === identifier);
  }

  assignValueToToken(identifier: string, value: any): void {
    for (const scope of this.scopes.slice().reverse()) {
      for (const currentToken of scope) {
        if (currentToken[2] === identifier) {
          currentToken[3] = value;
          return;
        }
      }
    }
  }

  processLine(line: string): void {
    line = line.trim().replace("\n", "");

    if (line.includes("BLOCO")) {
      this.block_identifiers.push(line.split(" ").pop()!);
      this.scopes.push([]);
      console.log(
        `\n*INICIO ${
          this.block_identifiers[this.block_identifiers.length - 1]
        }*`
      );
    } else if (
      this.block_identifiers.length &&
      new RegExp(
        `FIM${this.regex_whitespace}${
          this.block_identifiers[this.block_identifiers.length - 1]
        }`
      ).test(line)
    ) {
      if (this.scopes.length) {
        this.scopes.pop();
        console.log(
          `\n*FIM ${this.block_identifiers[this.block_identifiers.length - 1]}*`
        );
        this.block_identifiers.pop();
      }
    } else if (
      new RegExp(this.regex_declared_string).test(line) ||
      new RegExp(this.regex_declared_number).test(line)
    ) {
      if (line.includes(",")) {
        const [varType, rest] = line.split(" ", 2);
        const assignments = rest.split(",").map((s) => s.trim());
        assignments.forEach((assignment) => {
          const [id_current, value] = assignment
            .split("=")
            .map((s) => s.trim());
          if (
            !this.variableExists(
              id_current,
              this.scopes[this.scopes.length - 1]
            )
          ) {
            this.scopes[this.scopes.length - 1].push([
              "tk_identificador",
              varType,
              id_current,
              value || "0",
            ]);
          }
        });
      } else {
        const [varType, rest] = line.split(" ", 2);
        const [id_unique, value] = rest.split("=").map((s) => s.trim());
        if (
          !this.variableExists(id_unique, this.scopes[this.scopes.length - 1])
        ) {
          this.scopes[this.scopes.length - 1].push([
            "tk_identificador",
            varType,
            id_unique,
            value || "0",
          ]);
        }
      }
    } else if (
      new RegExp(this.regex_undeclared_string).test(line) ||
      new RegExp(this.regex_undeclared_number).test(line)
    ) {
      const [varType, id_unique] = line.split(" ").map((s) => s.trim());
      if (
        !this.variableExists(id_unique, this.scopes[this.scopes.length - 1])
      ) {
        this.scopes[this.scopes.length - 1].push([
          "tk_identificador",
          varType,
          id_unique,
          "0",
        ]);
      }
    } else if (new RegExp(this.regex_variable).test(line)) {
      const [id_a, id_b] = line.split("=").map((s) => s.trim());
      const token_b = this.getTokenByIdentifier(id_b);
      if (!token_b) {
        console.log(`${id_b} não declarado`);
        return;
      }
      const token_a = this.getTokenByIdentifier(id_a);
      if (!token_a) {
        this.scopes[this.scopes.length - 1].push([
          "tk_identificador",
          token_b[1],
          id_a,
          token_b[3],
        ]);
      } else {
        if (token_a[1] === token_b[1]) {
          this.assignValueToToken(id_a, token_b[3]);
        } else {
          console.log(`${id_a} : Atribuição inválida`);
        }
      }
    } else if (
      new RegExp(this.regex_variable_number).test(line) ||
      new RegExp(this.regex_variable_string).test(line)
    ) {
      const [id_a, value_a] = line.split("=").map((s) => s.trim());
      const token = this.getTokenByIdentifier(id_a);
      if (!token) {
        if (new RegExp(this.regex_number).test(value_a)) {
          this.scopes[this.scopes.length - 1].push([
            "tk_identificador",
            "NUMERO",
            id_a,
            value_a,
          ]);
        } else if (new RegExp(this.regex_string).test(value_a)) {
          this.scopes[this.scopes.length - 1].push([
            "tk_identificador",
            "CADEIA",
            id_a,
            value_a,
          ]);
        } else {
          console.log(`Error: Valor ou cadeia inválida.`);
        }
      } else {
        if (
          token[1] === "NUMERO" &&
          new RegExp(this.regex_number).test(value_a)
        ) {
          this.assignValueToToken(id_a, value_a);
        } else if (
          token[1] === "CADEIA" &&
          new RegExp(this.regex_string).test(value_a)
        ) {
          this.assignValueToToken(id_a, value_a);
        } else {
          console.log(`${id_a} : Atribuição inválida`);
        }
      }
    } else if (new RegExp(this.regex_print).test(line)) {
      const id_a = line.split(" ").pop();
      const token = this.getTokenByIdentifier(id_a!);
      if (!token) {
        console.log(`${id_a} não declarado`);
      } else {
        console.log(
          `${id_a} = ${token[3]} em ${
            this.block_identifiers[this.block_identifiers.length - 1]
          }`
        );
      }
    }
  }

  processScope(filePath: string): void {
    const lines = fs.readFileSync(filePath, "utf-8").split("\n");
    lines.forEach((line) => this.processLine(line));
  }
}

const manager = new ScopeManager();
manager.processScope("escopo.txt");
