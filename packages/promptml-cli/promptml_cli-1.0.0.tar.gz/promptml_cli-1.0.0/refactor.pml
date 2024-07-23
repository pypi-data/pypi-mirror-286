@prompt
    @context
        You are a master Python developer.
    @end

    @objective
        Migrate the below function from argparse to click.
        ```python
        def run():
            console = Console(
                color_system="truecolor",
                record=True,
            )
            neon_blue = Style(color="cyan", bold=True)

            arg_parser = argparse.ArgumentParser(
                        prog='promptml-cli',
                        description='A Command Line Interface (CLI) tool to run Prompt Markup Language (PromptML) files with popular Generative AI models',
                        epilog='For more details of composing PromptML files, visit: https://promptml.org/'
                    )

            arg_parser.add_argument('-f', '--file', type=str, help='Path to the PromptML(.pml) file', required=True)
            arg_parser.add_argument('-m', '--model', type=str, help='Model to use for the completion', default='gpt-4o')
            arg_parser.add_argument('-s', '--serializer', type=str, help='Serializer to use for the completion. Default is `xml`', default='xml', choices=['xml', 'json', 'yaml'])
            arg_parser.add_argument('-p', '--provider', type=str, help='GenAI provider to use for the completion. Default is `openai`', default=Provider.OPENAI.value, choices=[Provider.OPENAI.value, Provider.GOOGLE.value])
            arg_parser.add_argument('--stream', help='Stream chunks for the GenAI response. Default is non-streaming response.', action='store_true')
            arg_parser.add_argument('--raw', help='Return raw output from LLM (best for saving into files or piping)', action='store_true')

            args = arg_parser.parse_args()

            # Parse the PromptML file
            parser = PromptParserFromFile(args.file)
            parser.parse()

            serialized_data = None

            if args.serializer == "xml":
                serialized_data = parser.to_xml()
            elif args.serializer == "json":
                serialized_data = parser.to_json()
            elif args.serializer == "yaml":
                serialized_data = parser.to_yaml()
            else:
                serialized_data = parser.to_xml()


            now = time.time()
            if not args.stream:
                try:
                    response = get_sync_response(args, serialized_data)
                except APIConnectionError:
                    console.print(
                        "Error connecting to provider API. Try again! Please turn-off the VPN if needed.",
                        style = "bold red"
                    )
                    return
                # Print the completion with rich console
                if args.raw:
                    print(response)
                else:
                    console.print(Panel(Markdown(response, "\n")), soft_wrap=True, new_line_start=True)
            else:
                with Live(refresh_per_second=4) as live:
                    message = ""
                    for chunk in get_stream_response(args, serialized_data):
                        if chunk:
                            if args.raw:
                                print(chunk, end="")
                                continue
                            message += chunk
                            markdown_content = Markdown(message, "\n")
                            live.update(markdown_content)

            if not args.raw:
                time_taken = round(time.time() - now, 2)
                console.print(f"\nTime taken: {time_taken} seconds", style="bold green")
        ```
    @end
@end
