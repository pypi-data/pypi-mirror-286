from disnake.ext import commands


async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Не указан обязательный аргумент!", delete_after=3)

    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("Произошла ошибка при выполнении команды!", delete_after=3)

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Вы не обладаете достаточными правами для использования команды: `!{ctx.command}`", delete_after=3)

    else:
        await ctx.send(f"Произошла неизвестная ошибка: {str(error)}", delete_after=3)
