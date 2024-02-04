import { AstBuilder, Errors, GherkinClassicTokenMatcher, Parser } from "@cucumber/gherkin";
import { GherkinDocument, IdGenerator } from "@cucumber/messages";

const uuidFn = IdGenerator.uuid();

export type ParseResult = {
  gherkinDocument?: GherkinDocument;
  error?: Errors.GherkinException;
};

/**
 * Incrementally parses a Gherkin Document, allowing some syntax errors to occur.
 */
export function parseGherkinDocument(gherkinSource: string): ParseResult {
  const builder = new AstBuilder(uuidFn);
  const matcher = new GherkinClassicTokenMatcher();
  const parser = new Parser(builder, matcher);
  try {
    return {
      gherkinDocument: parser.parse(gherkinSource),
    };
  } catch (error) {
    let gherkinDocument: GherkinDocument;

    for (let i = 0; i < 10; i++) {
      gherkinDocument = builder.getResult();
      if (gherkinDocument) {
        return {
          gherkinDocument: gherkinDocument,
          error: error as Errors.GherkinException,
        };
      }

      try {
        builder.endRule();
      } catch (ignore) {
        // no-op
      }
    }

    return {
        error: error as Errors.GherkinException,
    };
  }
}
