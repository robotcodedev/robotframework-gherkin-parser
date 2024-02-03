import * as vscode from "vscode";

export async function activateAsync(_context: vscode.ExtensionContext): Promise<void> {
  const robotcode = vscode.extensions.getExtension("d-biehl.robotcode");
  if (!robotcode) {
    return;
  }
  await robotcode.activate();
  const robotcodeExtensionApi = robotcode.exports;
  if (!robotcodeExtensionApi) {
    return;
  }
}

function displayProgress<R>(promise: Promise<R>): Thenable<R> {
  const progressOptions: vscode.ProgressOptions = {
    location: vscode.ProgressLocation.Window,
    title: "RobotCode Gherkin extension loading ...",
  };
  return vscode.window.withProgress(progressOptions, () => promise);
}

export async function activate(context: vscode.ExtensionContext): Promise<void> {
  return displayProgress(activateAsync(context));
}

export async function deactivate(): Promise<void> {
  return Promise.resolve();
}
