import * as vscode from "vscode";
import { parseGherkinDocument } from "./parseGherkinDocument";
import { pretty } from "@cucumber/gherkin-utils";

export class GherkinFormattingEditProvider implements vscode.DocumentFormattingEditProvider {
  provideDocumentFormattingEdits(
    document: vscode.TextDocument,
    options: vscode.FormattingOptions,
    token: vscode.CancellationToken,
  ): vscode.ProviderResult<vscode.TextEdit[]> {
    const gherkinSource = document.getText();
    const { gherkinDocument } = parseGherkinDocument(gherkinSource);
    if (gherkinDocument === undefined) return [];
    const newText = pretty(gherkinDocument);
    const lines = gherkinSource.split(/\r?\n/);
    const line = lines.length - 1;
    const character = lines[line].length;
    const textEdit: vscode.TextEdit = new vscode.TextEdit(new vscode.Range(0, 0, line, character), newText);
    return [textEdit];
  }
}
